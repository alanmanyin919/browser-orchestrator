# Setup Guide

## Scope

This guide describes how to run the current repository as a local scaffold and how it maps to the two upstream projects it references:

- Playwright MCP as the intended primary browser backend.[1]
- `browser-use` as the intended fallback browser backend.[2]

The current codebase does not yet wire either backend end-to-end, so these steps are split into:

- local setup for this repository
- upstream runtime references you will likely integrate next

## Prerequisites

- Python 3.11+
- Node.js 18+
- `pip`
- `npx`

## 1. Install repository dependencies

From the repository root:

```bash
pip install -r requirements.txt
```

## 2. Start the orchestrator API

```bash
python adapter/app.py
```

The API defaults to `http://localhost:3101`.

Useful endpoints:

- `GET /health`
- `GET /mcp/tools`

## 3. Optional helper scripts

These scripts are useful for local development, but note that the primary and fallback scripts are placeholders today.

```bash
./scripts/start_primary.sh
./scripts/start_fallback.sh
./scripts/start_all.sh
./scripts/healthcheck.sh
```

## 4. Primary backend reference: Playwright MCP

The upstream Playwright MCP project documents a standard MCP configuration using `npx @playwright/mcp@latest`.[1]

Example MCP config:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

This repository currently points at `PLAYWRIGHT_MCP_URL=http://localhost:3100`, so if you implement the real adapter, keep the transport choice and startup story aligned with that URL or update the repo config accordingly.

## 5. Fallback backend reference: browser-use

The upstream `browser-use` project documents:

- Python 3.11+
- installation with `uv add browser-use`
- optional browser install with `uvx browser-use install`[2]

This repository does not yet contain the live fallback integration code; the fallback service wrapper is currently a placeholder abstraction around the future `browser-use` connection.

## 6. Verify the local scaffold

Check that the API is up:

```bash
curl http://localhost:3101/health
curl http://localhost:3101/mcp/tools
```

Run tests:

```bash
pytest tests/
```

## 7. Recommended next steps

To complete initialization beyond documentation:

1. Add a real `.env.example`.
2. Implement a real Playwright MCP client in [adapter/services/playwright_primary.py](../adapter/services/playwright_primary.py).
3. Implement a real `browser-use` client in [adapter/services/browser_use_fallback.py](../adapter/services/browser_use_fallback.py).
4. Update the start scripts so they launch real services instead of placeholders.
5. Add end-to-end tests against both backends.

## Citations

[1] Microsoft, "Playwright MCP", GitHub repository and setup documentation: https://github.com/microsoft/playwright-mcp

[2] browser-use, "browser-use", GitHub repository and quickstart documentation: https://github.com/browser-use/browser-use
