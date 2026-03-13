#!/bin/bash
# Configure browser-use main service

echo "Configuring browser-use main service..."

# Check if browser-use is installed
if ! pip show browser-use &> /dev/null; then
    echo "Warning: browser-use not installed. Install with: pip install browser-use"
fi

# Set environment
export LLM_PROVIDER=${LLM_PROVIDER:-minimax}
export MINIMAX_MODEL=${MINIMAX_MODEL:-MiniMax-M2.5}
export MINIMAX_BASE_URL=${MINIMAX_BASE_URL:-https://api.minimax.io/v1}
export BROWSER_USE_MAX_STEPS=${BROWSER_USE_MAX_STEPS:-12}
export MINIMAX_TIMEOUT_SECONDS=${MINIMAX_TIMEOUT_SECONDS:-90}
export FALLBACK_MODE=true

echo "LLM provider: $LLM_PROVIDER"
echo "MiniMax model: $MINIMAX_MODEL"
echo "MiniMax base URL: $MINIMAX_BASE_URL"
echo "browser-use max steps: $BROWSER_USE_MAX_STEPS"
echo "MiniMax timeout: $MINIMAX_TIMEOUT_SECONDS"
echo "Main browser-use configuration ready"

# browser-use runs in-process inside the app.
# This script exists only as a configuration helper.

# Keep script running
echo "browser-use helper running. Press Ctrl+C to stop."
tail -f /dev/null
