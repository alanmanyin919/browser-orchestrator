"""Minimal MiniMax wiring smoke check.

This script validates that MiniMax/OpenAI-compatible configuration can
construct the browser-use ChatOpenAI client and a browser-use Agent without
using browser-use cloud or running a full browsing task.
"""

from __future__ import annotations

import sys

from adapter.llm_factory import LLMConfigurationError, create_llm, resolve_llm_settings


def main() -> int:
    try:
        settings = resolve_llm_settings()
        llm = create_llm()

        from browser_use import Agent

        agent = Agent(task="Open a blank page and stop.", llm=llm)
        print("MiniMax configuration OK")
        print(f"provider={settings.provider}")
        print(f"model={settings.model}")
        print(f"base_url={settings.base_url}")
        print(f"agent_class={agent.__class__.__name__}")
        return 0
    except LLMConfigurationError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - runtime smoke path
        print(f"Smoke test failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
