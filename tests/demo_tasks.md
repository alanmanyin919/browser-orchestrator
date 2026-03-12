# Demo Tasks

Try these scenarios to test the browser orchestrator.

## Task 1: Simple Web Search

Search for a topic and get results.

```bash
curl -X POST http://localhost:3101/tools/web_search \
  -H "Content-Type: application/json" \
  -d '{"query": "Python programming"}'
```

Expected: JSON with search results, status "success", backend "playwright-mcp"

---

## Task 2: Open a Page

Open a specific URL.

```bash
curl -X POST http://localhost:3101/tools/open_page \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.python.org"}'
```

Expected: JSON with page info, status "success"

---

## Task 3: Extract Page Content

Get the content of a page.

```bash
curl -X POST http://localhost:3101/tools/extract_page \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.python.org"}'
```

Expected: JSON with extracted content

---

## Task 4: Read Top Results

Search and read multiple sources.

```bash
curl -X POST http://localhost:3101/tools/read_top_results \
  -H "Content-Type: application/json" \
  -d '{"query": "best Python frameworks", "max_results": 3}'
```

Expected: JSON with summaries of top 3 results

---

## Task 5: Navigate and Extract

Multi-step navigation task.

```bash
curl -X POST http://localhost:3101/tools/navigate_and_extract \
  -H "Content-Type: application/json" \
  -d '{"task": "Find the version number", "url": "https://www.python.org"}'
```

Expected: JSON with navigation result

---

## Task 6: Health Check

Check if all services are running.

```bash
curl http://localhost:3101/health
```

Expected: JSON with health status

---

## Task 7: List Tools

See all available tools.

```bash
curl http://localhost:3101/mcp/tools
```

Expected: JSON list of MCP tools

---

## Task 8: Test Blocked Page

Try to access a blocked page (should return blocked status).

```bash
curl -X POST http://localhost:3101/tools/open_page \
  -H "Content-Type: application/json" \
  -d '{"url": "https://accounts.google.com/signin"}'
```

Expected: JSON with status "blocked" or "restricted"

---

## Task 9: Test Fallback (Simulated)

The router automatically uses fallback when primary fails.

```bash
curl -X POST http://localhost:3101/tools/extract_page \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Check the "backend" field in response - could be either:
- "playwright-mcp" (primary)
- "better-browser-use" (fallback)

---

## Running All Tests

```bash
# Run pytest
pytest tests/ -v

# Or run manually
python -m tests.demo_tasks
```
