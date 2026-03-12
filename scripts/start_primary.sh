#!/bin/bash
# Start Playwright MCP Primary Service

echo "Starting Playwright MCP Primary Service..."

# Check if Playwright is installed
if ! command -v playwright &> /dev/null; then
    echo "Error: Playwright not found. Install with: pip install playwright"
    exit 1
fi

# Set environment
export PLAYWRIGHT_MCP_URL=${PLAYWRIGHT_MCP_URL:-http://localhost:3100}
export PRIMARY_MODE=true

echo "Playwright MCP URL: $PLAYWRIGHT_MCP_URL"
echo "Primary service ready"

# In production, would start actual Playwright MCP server here
# For now, this is a placeholder

# Keep script running
echo "Primary service running. Press Ctrl+C to stop."
tail -f /dev/null
