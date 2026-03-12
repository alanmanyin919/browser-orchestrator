# Architecture

## Overview

The Browser Orchestrator provides a unified browser automation interface for Clawbot.

```
┌─────────────────────────────────────────────────────────────┐
│                      Clawbot / LLM                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   MCP Tool Interface                        │
│   web_search | open_page | extract_page | read_top_results  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Router Layer                            │
│         (decides primary vs fallback)                       │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│   Primary Backend       │     │   Fallback Backend          │
│   ─────────────────     │     │   ──────────────────        │
│   Playwright MCP       │     │   better-browser-use        │
│                        │     │                              │
│   - Stable             │     │   - Complex pages            │
│   - Fast               │     │   - Multi-step workflows    │
│   - Default            │     │   - Dynamic content          │
└─────────────────────────┘     └─────────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Normalized Output                          │
│   { status, backend, title, url, summary, content, ... }   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Router (`adapter/router.py`)
- Decides which backend to use
- Implements fallback policy
- Checks stop conditions (CAPTCHA, login, etc.)
- Normalizes output from both backends

### Primary Service (`adapter/services/playwright_primary.py`)
- Playwright MCP integration
- Default backend for all operations
- Fast, stable browser automation

### Fallback Service (`adapter/services/browser_use_fallback.py`)
- Better-browser-use integration
- Used only when primary fails
- Handles complex dynamic pages

### Schemas (`adapter/schemas.py`)
- Standardized data models
- Normalized result format
- Health check models

## Data Flow

1. **Request arrives** → Router receives MCP tool call
2. **Try primary** → Playwright MCP attempts operation
3. **Check result** → Router evaluates if fallback needed
4. **Fallback if needed** → better-browser-use handles complex case
5. **Check stop conditions** → CAPTCHA/login detection
6. **Return normalized result** → Consistent output to caller

## Configuration

- `config/mcp.json` - MCP server configuration
- `config/browser-policy.yaml` - Routing rules and policies
- `config/app-config.yaml` - Application settings
- `.env` - Environment variables
