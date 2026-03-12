# Troubleshooting

## Common Issues

### 1. Primary service won't start

**Symptom**: Playwright MCP connection fails

**Solutions**:
```bash
# Check Playwright is installed
playwright --version

# Reinstall browsers
playwright install chromium

# Install system dependencies
playwright install-deps
```

### 2. Fallback service unavailable

**Symptom**: Better-browser-use not responding

**Solutions**:
```bash
# Check if installed
pip show browser-use

# Install or upgrade
pip install browser-use --upgrade

# Check it's running
curl http://localhost:8000/health
```

### 3. Port already in use

**Symptom**: `Address already in use` error

**Solutions**:
```bash
# Find process using port
lsof -i :3101

# Kill it or use different port
MCP_PORT=3102 python adapter/app.py
```

### 4. Slow performance

**Symptoms**: Timeouts, slow responses

**Solutions**:
- Check network connectivity
- Increase timeout in config
- Use headless mode (default)
- Close browser tabs between uses

### 5. CAPTCHA/blocks

**Symptom**: Always getting blocked

**Note**: This is expected behavior. The system correctly detects:
- CAPTCHA challenges
- Login walls
- Access restrictions

**Solution**: These pages are not suitable for automation. Use different sources or get proper API access.

## Debug Mode

Enable debug logging:

```bash
LOG_LEVEL=DEBUG python adapter/app.py
```

## Health Check

```bash
# Check service health
curl http://localhost:3101/health

# Expected response:
{
  "status": "healthy",
  "primary": true,
  "fallback": true,
  "uptime_seconds": 123.45,
  "version": "1.0.0"
}
```

## Test Scenarios

### Test 1: Basic search
```bash
curl -X POST http://localhost:3101/tools/web_search \
  -H "Content-Type: application/json" \
  -d '{"query": "Python tutorials"}'
```

### Test 2: Open page
```bash
curl -X POST http://localhost:3101/tools/open_page \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Test 3: Extract content
```bash
curl -X POST http://localhost:3101/tools/extract_page \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Logs

Check logs at:
- Console (stdout)
- `./logs/browser-orchestrator.log`

```bash
# Tail logs
tail -f logs/browser-orchestrator.log

# Search for errors
grep ERROR logs/browser-orchestrator.log
```

## Getting Help

If issues persist:
1. Check all services are running
2. Verify configuration in `.env`
3. Enable debug logging
4. Check firewall/network settings
5. Review the routing policy docs
