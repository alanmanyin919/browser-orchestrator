# Routing Policy

## Overview

The router chooses a preferred backend by tool type, then tries the secondary backend if the preferred result is failed, thin, or low-confidence.

## Preferred Backend By Tool

| Tool | Preferred backend | Secondary backend |
|------|-------------------|------------------|
| `web_search` | `browser-use` | Playwright MCP |
| `read_top_results` | `browser-use` | Playwright MCP |
| `navigate_and_extract` | `browser-use` | Playwright MCP |
| `open_page` | Playwright MCP | `browser-use` |
| `extract_page` | Playwright MCP | `browser-use` |

## Result Quality Rules

The router tries the secondary backend when:

- `status = "failed"`
- `confidence = "low"`
- `navigate_and_extract` cannot confirm the task outcome
- extracted content is missing
- extracted content is too thin to be useful

## Stop Conditions

The router returns blocked or restricted immediately for:

- CAPTCHA or human-verification pages
- login walls
- 403 / forbidden / access denied pages

## Practical Intent

- Use `browser-use` as the main access layer for research and multi-step browsing.
- Use Playwright for direct page opening and deterministic extraction.
- Preserve the same public API regardless of which backend answered.
