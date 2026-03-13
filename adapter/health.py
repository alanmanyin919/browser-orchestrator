"""
Health check module for browser orchestrator.
"""

import time
from .schemas import HealthStatus
from .logging_config import get_logger
from .services.playwright_primary import PlaywrightPrimaryService
from .services.browser_use_fallback import BrowserUseFallbackService

logger = get_logger("health")


class HealthChecker:
    """Monitors health of the main browser-use backend and Playwright secondary backend."""
    
    def __init__(self):
        self.start_time = time.time()
        self.primary_available = False
        self.fallback_available = False
        self.primary_service = BrowserUseFallbackService()
        self.fallback_service = PlaywrightPrimaryService()
    
    async def check_primary(self) -> bool:
        """Check if browser-use is available."""
        try:
            self.primary_available = self.primary_service.check_ready()
            return self.primary_available
        except Exception as e:
            logger.warning(f"Primary health check failed: {e}")
            self.primary_available = False
            return False
    
    async def check_fallback(self) -> bool:
        """Check if Playwright MCP is available."""
        try:
            self.fallback_available = await self.fallback_service.initialize()
            return self.fallback_available
        except Exception as e:
            logger.warning(f"Fallback health check failed: {e}")
            self.fallback_available = False
            return False
    
    async def check_health(self) -> HealthStatus:
        """Get overall health status."""
        primary_ok = await self.check_primary()
        fallback_ok = await self.check_fallback()
        
        uptime = time.time() - self.start_time
        
        if primary_ok and fallback_ok:
            status = "healthy"
        elif primary_ok or fallback_ok:
            status = "degraded"
        else:
            status = "unhealthy"
        
        return HealthStatus(
            status=status,
            primary=primary_ok,
            fallback=fallback_ok,
            uptime_seconds=uptime
        )


# Global health checker instance
_health_checker = HealthChecker()


def get_health_checker() -> HealthChecker:
    """Get the global health checker."""
    return _health_checker
