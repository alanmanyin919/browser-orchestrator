# Fallback Tool Usage - better-browser-use

## When It's Used

The router automatically uses fallback when:

1. **Primary extraction failed** - Couldn't get content
2. **Navigation got stuck** - Page didn't load properly
3. **Content is too dynamic** - Heavy JavaScript
4. **Multi-step workflows** - Complex interactions needed

## You Don't Choose It Directly

**The router decides.** Just use the normal tools and the system will fallback automatically if needed.

## When It Might Be Used

- Single-page applications
- Sites with complex interactions
- Pages that require scrolling/clicks
- Sites with lazy-loaded content

## What It Returns

Same normalized format as primary:

```json
{
  "status": "success",
  "backend": "better-browser-use",
  "title": "Page Title",
  "url": "https://example.com",
  "summary": "Short summary",
  "content": "Full content...",
  "key_points": ["Point 1", "Point 2"],
  "confidence": "medium",
  "metadata": {
    "used_fallback": true,
    "reason": "Dynamic content detected"
  }
}
```

## Note on Confidence

Fallback results typically have **medium confidence** because:
- Slower than primary
- More resource-intensive
- Still reliable, but less optimized

## Stop Conditions Apply

Even fallback won't proceed for:
- CAPTCHA challenges
- Login walls
- Access restrictions

Returns `blocked` or `restricted` instead.
