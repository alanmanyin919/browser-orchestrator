# Clawbot Browser Policy

## For Clawbot/LLM Agents

When you need browser automation, use this orchestrator.

## Tool Selection Guide

| Task | Use Tool |
|------|----------|
| Find information online | `web_search` |
| Visit a specific page | `open_page` |
| Get page content | `extract_page` |
| Research a topic | `read_top_results` |
| Complex navigation | `navigate_and_extract` |

## Important Rules

1. **Try simple tools first** - `web_search` is usually enough
2. **Primary is default** - Playwright MCP handles most cases
3. **Fallback is automatic** - Router decides if fallback needed
4. **Respect blocks** - If blocked, stop and report

## Don't

- Don't try to bypass CAPTCHA
- Don't try to bypass login walls
- Don't scrape restricted content
- Don't hammer the same site

## Response Format

All tools return:
```json
{
  "status": "success | failed | blocked | restricted",
  "backend": "playwright-mcp | better-browser-use",
  "title": "...",
  "url": "...",
  "summary": "...",
  "content": "...",
  "key_points": [...],
  "confidence": "high | medium | low",
  "error": "..."
}
```

## Example Usage

**Simple search:**
```
web_search(query="best Python frameworks 2024")
```

**Research topic:**
```
read_top_results(query="Python async programming", max_results=5)
```

**Get specific page:**
```
open_page(url="https://docs.python.org/3/")
```
