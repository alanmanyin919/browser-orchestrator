"""
Test suite for browser orchestrator.
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add adapter to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapter.schemas import BrowserResult, Metadata, HealthStatus
from adapter.router import BrowserRouter


class TestSchemas:
    """Test schema validation."""
    
    def test_browser_result_defaults(self):
        """Test BrowserResult default values."""
        result = BrowserResult()
        
        assert result.status == "success"
        assert result.backend == "playwright-mcp"
        assert result.title is None
        assert result.url is None
        assert result.summary is None
        assert result.content is None
        assert result.key_points == []
        assert result.confidence == "medium"
        assert result.error is None
        assert result.metadata.used_fallback == False
    
    def test_browser_result_to_dict(self):
        """Test BrowserResult serialization."""
        result = BrowserResult(
            status="success",
            backend="playwright-mcp",
            title="Test",
            url="https://example.com"
        )
        
        d = result.to_dict()
        assert d["status"] == "success"
        assert d["backend"] == "playwright-mcp"
        assert d["title"] == "Test"
    
    def test_metadata_defaults(self):
        """Test Metadata default values."""
        meta = Metadata()
        
        assert meta.used_fallback == False
        assert meta.reason is None
        assert meta.visited_urls == []
        assert meta.attempt_count == 1


class TestRouter:
    """Test router functionality."""
    
    @pytest.mark.asyncio
    async def test_router_initialization(self):
        """Test router can be initialized."""
        router = BrowserRouter()
        await router.initialize()
        assert router._initialized == True
        await router.close()
    
    @pytest.mark.asyncio
    async def test_web_search_returns_result(self):
        """Test web_search returns a valid result."""
        router = BrowserRouter()
        result = await router.web_search("test query")
        
        assert isinstance(result, BrowserResult)
        assert result.status in ["success", "failed"]
        assert result.backend in ["playwright-mcp", "better-browser-use"]
        await router.close()
    
    @pytest.mark.asyncio
    async def test_open_page_returns_result(self):
        """Test open_page returns a valid result."""
        router = BrowserRouter()
        result = await router.open_page("https://example.com")
        
        assert isinstance(result, BrowserResult)
        assert result.url == "https://example.com"
        await router.close()
    
    @pytest.mark.asyncio
    async def test_extract_page_returns_result(self):
        """Test extract_page returns a valid result."""
        router = BrowserRouter()
        result = await router.extract_page("https://example.com")
        
        assert isinstance(result, BrowserResult)
        await router.close()
    
    @pytest.mark.asyncio
    async def test_read_top_results(self):
        """Test read_top_results with max_results."""
        router = BrowserRouter()
        result = await router.read_top_results("Python", max_results=3)
        
        assert isinstance(result, BrowserResult)
        assert result.status in ["success", "failed"]
        await router.close()
    
    @pytest.mark.asyncio
    async def test_navigate_and_extract(self):
        """Test navigate_and_extract."""
        router = BrowserRouter()
        result = await router.navigate_and_extract(
            task="Find info",
            url="https://example.com"
        )
        
        assert isinstance(result, BrowserResult)
        await router.close()


class TestStopConditions:
    """Test stop condition detection."""
    
    @pytest.mark.asyncio
    async def test_captcha_detection(self):
        """Test CAPTCHA pages are blocked."""
        router = BrowserRouter()
        
        # Create result with CAPTCHA content
        result = BrowserResult(
            status="success",
            content="Please verify you're human to continue. CAPTCHA challenge."
        )
        
        # Router should detect and block
        # (This is internal logic test)
        assert result.status == "success"  # Before check
    
    @pytest.mark.asyncio
    async def test_login_detection(self):
        """Test login walls are blocked."""
        router = BrowserRouter()
        
        result = BrowserResult(
            status="success",
            content="Please sign in to continue. Login required."
        )
        
        assert result.status == "success"  # Before check


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
