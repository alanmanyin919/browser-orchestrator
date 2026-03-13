"""
LLM provider factory for browser-use integrations.

This module keeps provider configuration constructor-based and centralized so
the service layer does not need provider-specific wiring or monkey-patching.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


class LLMConfigurationError(RuntimeError):
    """Raised when provider configuration is incomplete or invalid."""


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    model: str
    api_key: str
    base_url: str
    timeout_seconds: int
    max_retries: int


def resolve_llm_settings(config: Optional[Dict[str, Any]] = None, provider: Optional[str] = None) -> LLMSettings:
    """Resolve provider configuration from explicit config and environment variables."""
    config = config or {}
    resolved_provider = (
        provider
        or config.get("provider")
        or os.getenv("LLM_PROVIDER")
        or "minimax"
    ).strip().lower()

    if resolved_provider != "minimax":
        raise LLMConfigurationError(
            f"Unsupported LLM provider '{resolved_provider}'. "
            "Only the self-hosted OpenAI-compatible 'minimax' provider is configured in this project."
        )

    model = _first_value(
        config.get("model"),
        os.getenv("LLM_MODEL"),
        os.getenv("MINIMAX_MODEL"),
        os.getenv("BROWSER_USE_MODEL"),
        "MiniMax-M2.5",
    )
    api_key = _first_value(
        config.get("api_key"),
        os.getenv("LLM_API_KEY"),
        os.getenv("MINIMAX_API_KEY"),
        os.getenv("BROWSER_USE_API_KEY"),
    )
    base_url = _first_value(
        config.get("base_url"),
        os.getenv("LLM_BASE_URL"),
        os.getenv("MINIMAX_BASE_URL"),
        os.getenv("BROWSER_USE_BASE_URL"),
        "https://api.minimax.io/v1",
    )
    timeout_seconds = int(
        _first_value(
            config.get("timeout_seconds"),
            os.getenv("LLM_TIMEOUT_SECONDS"),
            os.getenv("MINIMAX_TIMEOUT_SECONDS"),
            os.getenv("BROWSER_USE_TIMEOUT_SECONDS"),
            90,
        )
    )
    max_retries = int(
        _first_value(
            config.get("max_retries"),
            os.getenv("LLM_MAX_RETRIES"),
            os.getenv("MINIMAX_MAX_RETRIES"),
            2,
        )
    )

    if not api_key:
        raise LLMConfigurationError(
            "MiniMax configuration is missing MINIMAX_API_KEY. "
            "Set MINIMAX_API_KEY in your environment or .env file."
        )

    if not base_url:
        raise LLMConfigurationError(
            "MiniMax configuration is missing MINIMAX_BASE_URL. "
            "Set MINIMAX_BASE_URL to an OpenAI-compatible endpoint such as https://api.minimax.io/v1."
        )

    return LLMSettings(
        provider=resolved_provider,
        model=str(model),
        api_key=str(api_key),
        base_url=str(base_url),
        timeout_seconds=timeout_seconds,
        max_retries=max_retries,
    )


def create_llm(provider: str = "minimax", config: Optional[Dict[str, Any]] = None) -> Any:
    """Create a browser-use compatible chat model instance."""
    settings = resolve_llm_settings(config=config, provider=provider)
    ChatOpenAI = _load_chat_openai()
    return ChatOpenAI(
        model=settings.model,
        api_key=settings.api_key,
        base_url=settings.base_url,
        timeout=settings.timeout_seconds,
        max_retries=settings.max_retries,
        temperature=0,
    )


def _load_chat_openai() -> Callable[..., Any]:
    try:
        from browser_use import ChatOpenAI
    except ImportError as exc:
        raise LLMConfigurationError(
            "browser-use is required to create the MiniMax LLM client. "
            "Install dependencies from requirements.txt."
        ) from exc
    return ChatOpenAI


def _first_value(*values: Any) -> Any:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return None
