"""
Browser Router - Decides when to use primary vs fallback.

This is the brain of the orchestrator. It:
1. Tries primary first
2. Checks if fallback is needed
3. Returns normalized results
"""

import asyncio
from typing import Optional, Dict, Any
import yaml
from pathlib import Path

from .schemas import BrowserResult, Metadata
from .services.playwright_primary import PlaywrightPrimaryService
from .services.browser_use_fallback import BrowserUseFallbackService
from .logging_config import get_logger

logger = get_logger("router")


class BrowserRouter:
    """
    Routes browser requests to primary or fallback backends.
    
    Flow:
    1. Try primary (Playwright MCP)
    2. Check result against fallback policy
    3. If fallback needed, use better-browser-use
    4. Return normalized output
    """
    
    def __init__(self, config_path: str = "config/browser-policy.yaml"):
        # Load routing policy
        policy_file = Path(config_path)
        if policy_file.exists():
            with open(policy_file) as f:
                self.policy = yaml.safe_load(f)
        else:
            self.policy = self._default_policy()
        
        # Initialize services
        self.primary = PlaywrightPrimaryService()
        self.fallback = BrowserUseFallbackService()
        
        # Config
        self.max_retries = self.policy.get("primary", {}).get("max_retries", 2)
        self.fallback_enabled = True
        
        self._initialized = False
    
    def _default_policy(self) -> Dict:
        """Default routing policy."""
        return {
            "primary": {
                "name": "playwright-mcp",
                "timeout_seconds": 30,
                "max_retries": 2
            },
            "fallback": {
                "name": "better-browser-use",
                "timeout_seconds": 60,
                "max_retries": 1
            },
            "fallback_triggers": [
                {"type": "extraction_failed", "description": "Primary extraction failed"},
                {"type": "navigation_stuck", "description": "Primary navigation got stuck"},
                {"type": "dynamic_content", "description": "Page content too dynamic"}
            ],
            "stop_conditions": [
                {"type": "captcha", "action": "blocked"},
                {"type": "login_required", "action": "blocked"},
                {"type": "access_denied", "action": "restricted"}
            ]
        }
    
    async def initialize(self):
        """Initialize both backends."""
        if self._initialized:
            return
        
        logger.info("Initializing browser router...")
        
        # Initialize primary
        primary_ok = await self.primary.initialize()
        logger.info(f"Primary backend: {'OK' if primary_ok else 'FAILED'}")
        
        # Initialize fallback
        fallback_ok = await self.fallback.initialize()
        logger.info(f"Fallback backend: {'OK' if fallback_ok else 'FAILED'}")
        
        self._initialized = True
        logger.info("Browser router initialized")
    
    def _should_use_fallback(self, result: BrowserResult, reason: str = "") -> bool:
        """
        Determine if fallback should be used based on result.
        
        Returns True if:
        - Primary failed
        - Extraction was incomplete
        - Navigation got stuck
        """
        if not self.fallback_enabled:
            return False
        
        # Check for failure
        if result.status == "failed":
            logger.info(f"Fallback trigger: Primary failed - {result.error}")
            return True
        
        # Check for incomplete content
        if result.status == "success" and result.content:
            if len(result.content) < 100 and "placeholder" in result.content.lower():
                logger.info("Fallback trigger: Incomplete content detected")
                return True
        
        # Check for low confidence
        if result.confidence == "low":
            logger.info("Fallback trigger: Low confidence result")
            return True
        
        return False
    
    def _check_stop_conditions(self, result: BrowserResult) -> BrowserResult:
        """
        Check if we should stop due to anti-bot measures.
        
        Returns modified result with blocked/restricted status if needed.
        """
        content = (result.content or "").lower()
        url = (result.url or "").lower()
        combined = content + url
        
        stop_conditions = self.policy.get("stop_conditions", [])
        
        for condition in stop_conditions:
            condition_type = condition.get("type", "")
            action = condition.get("action", "blocked")
            
            # Check for CAPTCHA
            if condition_type == "captcha":
                if any(x in combined for x in ["captcha", "recaptcha", "verify you're human"]):
                    logger.warning("Stop condition: CAPTCHA detected")
                    result.status = "blocked"
                    result.error = "CAPTCHA challenge detected - stopping"
                    return result
            
            # Check for login required
            if condition_type == "login_required":
                if any(x in combined for x in ["sign in", "login required", "please sign in"]):
                    if "captcha" not in combined:  # Not a captcha page
                        logger.warning("Stop condition: Login required")
                        result.status = "blocked"
                        result.error = "Login required to access this content"
                        return result
            
            # Check for access denied
            if condition_type == "access_denied":
                if any(x in combined for x in ["403", "forbidden", "access denied", "blocked"]):
                    logger.warning("Stop condition: Access denied")
                    result.status = "restricted"
                    result.error = "Access denied to this resource"
                    return result
        
        return result
    
    async def web_search(self, query: str, max_results: int = 5) -> BrowserResult:
        """Web search with automatic fallback."""
        await self.initialize()
        
        logger.info(f"Router: web_search for '{query}'")
        
        # Try primary first
        result = await self.primary.web_search(query, max_results)
        
        # Check stop conditions
        result = self._check_stop_conditions(result)
        if result.status in ["blocked", "restricted"]:
            return result
        
        # Check if fallback needed
        if self._should_use_fallback(result):
            logger.info("Router: Falling back to better-browser-use")
            result = await self.fallback.web_search(query, max_results)
            result = self._check_stop_conditions(result)
        
        return result
    
    async def open_page(self, url: str) -> BrowserResult:
        """Open a page with automatic fallback."""
        await self.initialize()
        
        logger.info(f"Router: open_page {url}")
        
        result = await self.primary.open_page(url)
        
        result = self._check_stop_conditions(result)
        if result.status in ["blocked", "restricted"]:
            return result
        
        if self._should_use_fallback(result):
            logger.info("Router: Falling back")
            result = await self.fallback.open_page(url)
            result = self._check_stop_conditions(result)
        
        return result
    
    async def extract_page(self, url: Optional[str] = None) -> BrowserResult:
        """Extract page content with automatic fallback."""
        await self.initialize()
        
        logger.info(f"Router: extract_page")
        
        result = await self.primary.extract_page(url)
        
        result = self._check_stop_conditions(result)
        if result.status in ["blocked", "restricted"]:
            return result
        
        if self._should_use_fallback(result):
            logger.info("Router: Falling back")
            result = await self.fallback.extract_page(url)
            result = self._check_stop_conditions(result)
        
        return result
    
    async def read_top_results(self, query: str, max_results: int = 3) -> BrowserResult:
        """Read top results with automatic fallback."""
        await self.initialize()
        
        logger.info(f"Router: read_top_results '{query}' (max={max_results})")
        
        result = await self.primary.read_top_results(query, max_results)
        
        result = self._check_stop_conditions(result)
        if result.status in ["blocked", "restricted"]:
            return result
        
        if self._should_use_fallback(result):
            logger.info("Router: Falling back")
            result = await self.fallback.read_top_results(query, max_results)
            result = self._check_stop_conditions(result)
        
        return result
    
    async def navigate_and_extract(self, task: str, url: str) -> BrowserResult:
        """Navigate and extract with automatic fallback."""
        await self.initialize()
        
        logger.info(f"Router: navigate_and_extract - {task}")
        
        result = await self.primary.navigate_and_extract(task, url)
        
        result = self._check_stop_conditions(result)
        if result.status in ["blocked", "restricted"]:
            return result
        
        if self._should_use_fallback(result):
            logger.info("Router: Falling back")
            result = await self.fallback.navigate_and_extract(task, url)
            result = self._check_stop_conditions(result)
        
        return result
    
    async def close(self):
        """Clean up resources."""
        await self.primary.close()
        await self.fallback.close()


# Global router instance
_router: Optional[BrowserRouter] = None


def get_router() -> BrowserRouter:
    """Get the global router instance."""
    global _router
    if _router is None:
        _router = BrowserRouter()
    return _router
