# Routing Policy

## Overview

The router decides which backend to use based on:
1. Success/failure of primary
2. Quality of extracted content
3. Stop conditions

## Default Behavior

### Step 1: Try Primary First

**Always try Playwright MCP first.** It is:
- Faster
- More stable
- Better for simple tasks

### Step 2: Evaluate Result

After primary completes, check:

| Condition | Action |
|-----------|--------|
| `status = "success"` with good content | Return result |
| `status = "failed"` | Try fallback |
| Content too short (<100 chars) | Try fallback |
| `confidence = "low"` | Try fallback |

### Step 3: Use Fallback (if needed)

Fallback to better-browser-use when:
- Primary extraction failed
- Navigation got stuck
- Page content is too dynamic
- Multi-step workflow needed

### Step 4: Check Stop Conditions

**Never fallback for these** - return blocked/restricted:

| Condition | Response |
|-----------|----------|
| CAPTCHA detected | `status: "blocked"` |
| Login required | `status: "blocked"` |
| Human verification | `status: "blocked"` |
| 403/Forbidden | `status: "restricted"` |
| Access denied | `status: "restricted"` |

## Fallback Triggers

The router triggers fallback when:

1. **Extraction Failed** - Primary couldn't extract meaningful content
2. **Navigation Stuck** - Page didn't load or got stuck
3. **Dynamic Content** - Content requires JavaScript execution beyond primary's capability
4. **Multi-step** - Task requires multiple page interactions

## Stop Conditions

These conditions cause immediate return with blocked/restricted status:

- **CAPTCHA** - reCAPTCHA, hCaptcha, etc.
- **Login Wall** - Sign in required
- **Human Verification** - "Verify you're human"
- **Access Denied** - 403 Forbidden, blocked IP
- **Rate Limited** - Too many requests

## Configuration

Edit `config/browser-policy.yaml` to customize:

```yaml
primary:
  timeout_seconds: 30
  max_retries: 2

fallback:
  timeout_seconds: 60
  max_retries: 1

fallback_triggers:
  - type: "extraction_failed"
  - type: "dynamic_content"

stop_conditions:
  - type: "captcha"
    action: "blocked"
  - type: "login_required"
    action: "blocked"
```

## Code Flow

```
Request → Primary.execute()
           │
           ▼
      Success? ──No──→ Check stop conditions
        │                   │
       Yes                  ▼
        │            Return blocked/restricted
        │
        ▼
   Good content? ──No──→ Fallback.execute()
        │                     │
       Yes                    ▼
        │              Check stop conditions
        │                     │
        ▼                     ▼
   Return result       Return result
```
