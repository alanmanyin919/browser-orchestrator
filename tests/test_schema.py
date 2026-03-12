"""
Test schema validation.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from adapter.schemas import (
    BrowserResult, 
    Metadata, 
    SearchResult, 
    SearchResponse,
    HealthStatus
)


class TestBrowserResult:
    """Test BrowserResult schema."""
    
    def test_default_values(self):
        """Test default values."""
        result = BrowserResult()
        
        assert result.status == "success"
        assert result.backend == "playwright-mcp"
        assert result.confidence == "medium"
        assert result.key_points == []
    
    def test_with_values(self):
        """Test with custom values."""
        result = BrowserResult(
            status="failed",
            backend="better-browser-use",
            title="Test Title",
            url="https://example.com",
            summary="Test summary",
            content="Test content",
            key_points=["Point 1", "Point 2"],
            confidence="high",
            error="Test error"
        )
        
        assert result.status == "failed"
        assert result.backend == "better-browser-use"
        assert result.title == "Test Title"
        assert len(result.key_points) == 2
    
    def test_to_dict(self):
        """Test serialization to dict."""
        result = BrowserResult(
            status="success",
            title="Test"
        )
        
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["status"] == "success"
        assert d["title"] == "Test"


class TestMetadata:
    """Test Metadata schema."""
    
    def test_defaults(self):
        """Test default metadata."""
        meta = Metadata()
        
        assert meta.used_fallback == False
        assert meta.reason is None
        assert meta.visited_urls == []
        assert meta.attempt_count == 1
    
    def test_with_values(self):
        """Test custom metadata."""
        meta = Metadata(
            used_fallback=True,
            reason="Dynamic content",
            visited_urls=["https://a.com", "https://b.com"],
            attempt_count=2
        )
        
        assert meta.used_fallback == True
        assert meta.reason == "Dynamic content"
        assert len(meta.visited_urls) == 2
        assert meta.attempt_count == 2


class TestSearchResult:
    """Test SearchResult schema."""
    
    def test_search_result(self):
        """Test search result item."""
        item = SearchResult(
            title="Result Title",
            url="https://example.com",
            snippet="Result snippet..."
        )
        
        assert item.title == "Result Title"
        assert item.url == "https://example.com"


class TestSearchResponse:
    """Test SearchResponse schema."""
    
    def test_search_response(self):
        """Test search response."""
        results = [
            SearchResult(title="A", url="https://a.com", snippet="..."),
            SearchResult(title="B", url="https://b.com", snippet="...")
        ]
        
        response = SearchResponse(
            query="test",
            results=results,
            total_results=100
        )
        
        assert response.query == "test"
        assert len(response.results) == 2
        assert response.total_results == 100


class TestHealthStatus:
    """Test HealthStatus schema."""
    
    def test_healthy(self):
        """Test healthy status."""
        status = HealthStatus(
            status="healthy",
            primary=True,
            fallback=True,
            uptime_seconds=100.0
        )
        
        assert status.status == "healthy"
        assert status.primary == True
        assert status.fallback == True
    
    def test_degraded(self):
        """Test degraded status."""
        status = HealthStatus(
            status="degraded",
            primary=True,
            fallback=False,
            uptime_seconds=50.0
        )
        
        assert status.status == "degraded"
        assert status.primary == True
        assert status.fallback == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
