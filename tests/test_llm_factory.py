"""Tests for MiniMax/OpenAI-compatible LLM factory wiring."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from adapter.llm_factory import LLMConfigurationError, create_llm, resolve_llm_settings


class DummyChatOpenAI:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


def test_resolve_llm_settings_prefers_minimax_env(monkeypatch):
    monkeypatch.setenv("MINIMAX_API_KEY", "test-key")
    monkeypatch.setenv("MINIMAX_BASE_URL", "https://api.minimax.io/v1")
    monkeypatch.setenv("MINIMAX_MODEL", "MiniMax-M2.5")

    settings = resolve_llm_settings()

    assert settings.provider == "minimax"
    assert settings.api_key == "test-key"
    assert settings.base_url == "https://api.minimax.io/v1"
    assert settings.model == "MiniMax-M2.5"


def test_create_llm_uses_browser_use_chat_openai(monkeypatch):
    monkeypatch.setenv("MINIMAX_API_KEY", "test-key")
    monkeypatch.setenv("MINIMAX_BASE_URL", "https://api.minimax.io/v1")
    monkeypatch.setenv("MINIMAX_MODEL", "MiniMax-M2.5")
    monkeypatch.setattr("adapter.llm_factory._load_chat_openai", lambda: DummyChatOpenAI)

    llm = create_llm()

    assert isinstance(llm, DummyChatOpenAI)
    assert llm.kwargs["model"] == "MiniMax-M2.5"
    assert llm.kwargs["api_key"] == "test-key"
    assert llm.kwargs["base_url"] == "https://api.minimax.io/v1"


def test_create_llm_fails_fast_when_api_key_missing(monkeypatch):
    monkeypatch.delenv("MINIMAX_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("BROWSER_USE_API_KEY", raising=False)

    with pytest.raises(LLMConfigurationError) as exc_info:
        resolve_llm_settings()

    assert "MINIMAX_API_KEY" in str(exc_info.value)
