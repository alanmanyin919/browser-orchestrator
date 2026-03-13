#!/bin/bash
# Configure Playwright MCP secondary service

echo "Configuring Playwright MCP secondary service..."

# Check if Playwright is installed
if ! command -v playwright &> /dev/null; then
    echo "Error: Playwright not found. Install with: pip install playwright"
    exit 1
fi

# Set environment
export PLAYWRIGHT_MCP_COMMAND=${PLAYWRIGHT_MCP_COMMAND:-npx}
export PLAYWRIGHT_MCP_ARGS=${PLAYWRIGHT_MCP_ARGS:-@playwright/mcp@latest}
export PLAYWRIGHT_MCP_TIMEOUT_SECONDS=${PLAYWRIGHT_MCP_TIMEOUT_SECONDS:-45}
export PLAYWRIGHT_HEADLESS=${PLAYWRIGHT_HEADLESS:-true}
export PRIMARY_MODE=true

echo "Playwright MCP command: $PLAYWRIGHT_MCP_COMMAND $PLAYWRIGHT_MCP_ARGS"
echo "Playwright MCP timeout: $PLAYWRIGHT_MCP_TIMEOUT_SECONDS"
echo "Playwright headless: $PLAYWRIGHT_HEADLESS"
echo "Secondary Playwright configuration ready"

# The app starts Playwright MCP per request over stdio.
# This script exists only as a configuration helper.

# Keep script running
echo "Playwright helper running. Press Ctrl+C to stop."
tail -f /dev/null
