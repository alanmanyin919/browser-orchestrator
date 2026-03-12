# Clawbot Browser Orchestrator

Browser orchestration layer for Clawbot/OpenClaw. This service exposes a single MCP-style HTTP surface and routes browser tasks between a primary Playwright MCP backend and a fallback `browser-use` backend.[1][2]

## Status

This repository is currently an orchestration scaffold:

- The FastAPI service, router, schemas, config, prompts, and tests are present.
- The backend service wrappers in [adapter/services/playwright_primary.py](adapter/services/playwright_primary.py) and [adapter/services/browser_use_fallback.py](adapter/services/browser_use_fallback.py) still return placeholder data rather than calling live upstream APIs.
- The shell scripts start the orchestrator and placeholder primary/fallback processes, but do not yet boot a real Playwright MCP server or a real `browser-use` worker.

If you use this repo today, treat it as a documented starter project rather than a production-ready browser automation gateway.

## What This Project Does

The orchestrator gives Clawbot a consistent interface for browser actions:

```text
Clawbot / LLM
  -> Browser Orchestrator API
  -> Router
     -> Primary: Playwright MCP
     -> Fallback: browser-use
  -> Normalized BrowserResult
```

Core goals:

- Prefer a stable default backend for ordinary browsing tasks.
- Fall back to a more agentic browser system when the primary result is incomplete or fails.
- Return a normalized result shape regardless of backend.
- Keep routing rules, stop conditions, and prompts in repo-managed config/docs.

## Current API Surface

The FastAPI app in [adapter/app.py](adapter/app.py) exposes:

- `POST /tools/web_search`
- `POST /tools/open_page`
- `POST /tools/extract_page`
- `POST /tools/read_top_results`
- `POST /tools/navigate_and_extract`
- `GET /health`
- `GET /mcp/tools`

The normalized response model lives in [adapter/schemas.py](adapter/schemas.py).

## Repository Layout

```text
clawbot-browser-orchestrator/
├── adapter/              # FastAPI app, router, schemas, service wrappers
├── config/               # Routing policy, app config, MCP config
├── docs/                 # Setup, architecture, routing, troubleshooting
├── prompts/              # Backend usage guidance for the agent
├── scripts/              # Local start and health scripts
├── tests/                # Schema/router tests and demo task notes
├── requirements.txt
└── package.json
```

## Local Setup

### Requirements

- Python 3.11+
- Node.js 18+
- A Playwright MCP runtime[1]
- A `browser-use` runtime if you want to implement the fallback backend[2]

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the orchestrator

```bash
python adapter/app.py
```

Default port: `3101`

### Optional local helper scripts

```bash
./scripts/start_primary.sh
./scripts/start_fallback.sh
./scripts/start_all.sh
./scripts/healthcheck.sh
```

Important: the `start_primary.sh` and `start_fallback.sh` scripts are placeholders in the current repo. They validate local tooling and hold a process open, but they do not yet launch the real upstream services.

## Suggested Upstream Integration Targets

### Primary backend: Playwright MCP

The current docs in the upstream Playwright MCP repository show the standard MCP config using `npx @playwright/mcp@latest`.[1]

Example:

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

### Fallback backend: browser-use

The upstream `browser-use` project documents Python 3.11+, installation via `uv add browser-use`, and optional browser installation with `uvx browser-use install`.[2]

This repository currently depends on `browser-use` conceptually, but does not yet include the live adapter code needed to drive a real fallback session.

## Configuration

Main config files:

- [config/browser-policy.yaml](config/browser-policy.yaml): primary/fallback names, timeouts, triggers, stop conditions
- [config/app-config.yaml](config/app-config.yaml): app-level settings
- [config/mcp.json](config/mcp.json): MCP-related config stub

Common runtime environment variables used by the scripts/app:

- `MCP_PORT` defaults to `3101`
- `PLAYWRIGHT_MCP_URL` defaults to `http://localhost:3100`
- `BROWSER_USE_API_URL` defaults to `http://localhost:8000`

## Documentation

- [docs/setup.md](docs/setup.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/routing-policy.md](docs/routing-policy.md)
- [docs/troubleshooting.md](docs/troubleshooting.md)

## Next Implementation Steps

To turn this scaffold into a working service:

1. Replace the placeholder Playwright wrapper with real MCP transport calls.
2. Replace the placeholder `browser-use` wrapper with a real agent/session integration.
3. Add environment examples for local and production deployment.
4. Add end-to-end tests against live upstream services.
5. Decide whether the fallback target is the official `browser-use` package or a specific internal fork, then rename the code/docs consistently.

## Citations

[1] Microsoft, "Playwright MCP", GitHub repository and setup documentation: https://github.com/microsoft/playwright-mcp

[2] browser-use, "browser-use", GitHub repository and quickstart documentation: https://github.com/browser-use/browser-use
