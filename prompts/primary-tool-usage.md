# Primary Tool Usage - Playwright MCP

## When to Use

Playwright MCP is your **default choice**. Use it for:

- Simple web searches
- Reading static pages
- Basic navigation
- Fast information retrieval
- Most common browser tasks

## Why Primary?

- ✅ Fast
- ✅ Stable
- ✅ Well-supported
- ✅ Good for 90% of tasks

## Usage Examples

### Web Search
```python
# Search and get results
result = await router.web_search("Python tutorials")
```

### Open Page
```python
# Open a URL
result = await router.open_page("https://example.com")
```

### Extract Content
```python
# Get page content
result = await router.extract_page("https://example.com")
```

### Read Top Results
```python
# Search and read multiple sources
result = await router.read_top_results("best Python books", max_results=3)
```

### Navigate & Extract
```python
# Multi-step task
result = await router.navigate_and_extract(
    task="Find the contact form",
    url="https://example.com/contact"
)
```

## Expected Output

```json
{
  "status": "success",
  "backend": "playwright-mcp",
  "title": "Page Title",
  "url": "https://example.com",
  "summary": "Short summary",
  "content": "Full content...",
  "key_points": ["Point 1", "Point 2"],
  "confidence": "high"
}
```

## When It Might Fail

- Complex JavaScript pages
- Heavy dynamic content
- Multi-step workflows

**That's okay** - the router will automatically try the fallback.
