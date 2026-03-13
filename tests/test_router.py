"""Behavioral tests for router backend selection and stop-condition logic."""

import sys
from pathlib import Path
from typing import Optional

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from adapter.router import BrowserRouter
from adapter.schemas import BrowserResult, Metadata


def _result(
    *,
    status: str = "success",
    backend: str = "playwright-mcp",
    content: Optional[str] = None,
    confidence: str = "high",
    error: Optional[str] = None,
    url: Optional[str] = "https://example.com",
    used_fallback: bool = False,
    reason: Optional[str] = None,
):
    return BrowserResult(
        status=status,
        backend=backend,
        title="Example",
        url=url,
        summary="Summary",
        content=content,
        key_points=["Point 1"],
        confidence=confidence,
        error=error,
        metadata=Metadata(
            used_fallback=used_fallback,
            reason=reason,
            visited_urls=[url] if url else [],
            attempt_count=1,
        ),
    )


class TestRouterFallbacks:
    @pytest.mark.asyncio
    async def test_router_initialization_tracks_backend_availability(self, monkeypatch):
        router = BrowserRouter()

        async def primary_init():
            return True

        async def fallback_init():
            return False

        monkeypatch.setattr(router.primary, "initialize", primary_init)
        monkeypatch.setattr(router.fallback, "initialize", fallback_init)

        await router.initialize()

        assert router._initialized is True
        assert router.primary_available is True
        assert router.fallback_available is False
        assert router.fallback_enabled is False

    @pytest.mark.asyncio
    async def test_web_search_prefers_browser_use(self, monkeypatch):
        router = BrowserRouter()
        router._initialized = True
        router.fallback_enabled = True

        async def primary_search(query, max_results):
            return _result(
                backend="better-browser-use",
                content="Primary browser-use search produced rich results.",
                confidence="high",
                used_fallback=True,
                reason="Main browser-use path",
            )

        async def fallback_search(query, max_results):
            raise AssertionError("Playwright should not be called for successful web_search")

        monkeypatch.setattr(router.primary, "web_search", primary_search)
        monkeypatch.setattr(router.fallback, "web_search", fallback_search)

        result = await router.web_search("test query")

        assert result.backend == "better-browser-use"

    @pytest.mark.asyncio
    async def test_extract_page_prefers_playwright_and_falls_back_to_browser_use(self, monkeypatch):
        router = BrowserRouter()
        router._initialized = True
        router.fallback_enabled = True

        async def secondary_extract(url):
            return _result(content="Too short", confidence="medium", url=url)

        async def primary_extract(url):
            return _result(
                backend="better-browser-use",
                content="This is a much richer fallback extraction result with enough content to pass.",
                confidence="medium",
                url=url,
                used_fallback=True,
                reason="Fallback used for dynamic content extraction",
            )

        monkeypatch.setattr(router.fallback, "extract_page", secondary_extract)
        monkeypatch.setattr(router.primary, "extract_page", primary_extract)

        result = await router.extract_page("https://example.com")

        assert result.backend == "better-browser-use"
        assert result.metadata.used_fallback is True

    @pytest.mark.asyncio
    async def test_navigate_and_extract_falls_back_on_low_confidence(self, monkeypatch):
        router = BrowserRouter()
        router._initialized = True
        router.fallback_enabled = True

        async def primary_nav(task, url):
            return _result(
                backend="better-browser-use",
                content="Loaded page text but task not confirmed.",
                confidence="low",
                url=url,
                used_fallback=True,
                reason="Task resolution not confirmed",
            )

        async def fallback_nav(task, url):
            return _result(
                backend="playwright-mcp",
                content="Secondary Playwright extraction completed successfully.",
                confidence="high",
                url=url,
                used_fallback=False,
                reason="Secondary Playwright path",
            )

        monkeypatch.setattr(router.primary, "navigate_and_extract", primary_nav)
        monkeypatch.setattr(router.fallback, "navigate_and_extract", fallback_nav)

        result = await router.navigate_and_extract("Find pricing", "https://example.com")

        assert result.backend == "playwright-mcp"
        assert result.confidence == "high"

    @pytest.mark.asyncio
    async def test_open_page_stays_primary_when_successful(self, monkeypatch):
        router = BrowserRouter()
        router._initialized = True
        router.fallback_enabled = True

        async def fallback_open(url):
            return _result(content=None, confidence="high", url=url)

        async def primary_open(url):
            raise AssertionError("browser-use should not be called for successful open_page")

        monkeypatch.setattr(router.fallback, "open_page", fallback_open)
        monkeypatch.setattr(router.primary, "open_page", primary_open)

        result = await router.open_page("https://example.com")

        assert result.backend == "playwright-mcp"


class TestStopConditions:
    def test_captcha_pages_are_blocked(self):
        router = BrowserRouter()
        result = _result(content="Please verify you're human. CAPTCHA required.")

        checked = router._check_stop_conditions(result)

        assert checked.status == "blocked"
        assert "CAPTCHA" in checked.error

    def test_login_pages_are_blocked(self):
        router = BrowserRouter()
        result = _result(content="Please sign in to continue. Login required.")

        checked = router._check_stop_conditions(result)

        assert checked.status == "blocked"
        assert "Login required" in checked.error

    def test_access_denied_pages_are_restricted(self):
        router = BrowserRouter()
        result = _result(content="403 forbidden. access denied.")

        checked = router._check_stop_conditions(result)

        assert checked.status == "restricted"
        assert "Access denied" in checked.error
