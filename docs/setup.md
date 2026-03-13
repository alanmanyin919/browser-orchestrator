# Setup Guide

## Scope

This guide describes how to run the current repository and how it maps to the two upstream projects it references:

- `browser-use` as the main browser backend.[2]
- Playwright MCP as the secondary backend for direct page access.[1]

The current codebase now includes concrete integrations for both backends. Local setup is mostly about installing dependencies and providing the required environment variables.

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

## 2. Configure environment

Create a local env file:

```bash
cp .env.example .env
```

Required main backend configuration:

- `MINIMAX_API_KEY`
- `MINIMAX_BASE_URL`
- `MINIMAX_MODEL`

The main `browser-use` path assumes an OpenAI-compatible endpoint, which can point at MiniMax.

## 3. Start the orchestrator API

```bash
python3 adapter/app.py
```

The API defaults to `http://localhost:3101`.

Useful endpoints:

- `GET /health`
- `GET /mcp/tools`

## 4. Optional helper scripts

These scripts are useful for local development, but note that they are configuration helpers rather than full service launchers.

```bash
./scripts/start_primary.sh
./scripts/start_fallback.sh
./scripts/start_all.sh
./scripts/healthcheck.sh
```

## 5. Secondary backend reference: Playwright MCP

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

This repository starts Playwright MCP locally via stdio. The main controls are:

- `PLAYWRIGHT_MCP_COMMAND`
- `PLAYWRIGHT_MCP_ARGS`
- `PLAYWRIGHT_MCP_TIMEOUT_SECONDS`
- `PLAYWRIGHT_HEADLESS`

## 6. Main backend reference: browser-use

The upstream `browser-use` project documents:

- Python 3.11+
- installation with `uv add browser-use`
- optional browser install with `uvx browser-use install`[2]

This repository uses `browser-use` directly in-process as the main execution backend. The main controls are:

- `LLM_PROVIDER`
- `MINIMAX_MODEL`
- `MINIMAX_API_KEY`
- `MINIMAX_BASE_URL`
- `MINIMAX_TIMEOUT_SECONDS`
- `MINIMAX_MAX_RETRIES`
- `BROWSER_USE_MAX_STEPS`

## 7. Verify the local service

Check that the API is up:

```bash
curl http://localhost:3101/health
curl http://localhost:3101/mcp/tools
```

Run tests:

```bash
python3 -m pytest tests/
```

Run the MiniMax wiring smoke check:

```bash
python3 scripts/smoke_minimax.py
```

## 8. Recommended next steps

After local setup:

1. Verify MiniMax accepts the configured `MINIMAX_MODEL` and `MINIMAX_BASE_URL`.
2. Verify the Playwright MCP runtime exposes the expected tools in your environment.
3. Add live integration tests for both backends before production use.

## Citations

[1] Microsoft, "Playwright MCP", GitHub repository and setup documentation: https://github.com/microsoft/playwright-mcp

[2] browser-use, "browser-use", GitHub repository and quickstart documentation: https://github.com/browser-use/browser-use
