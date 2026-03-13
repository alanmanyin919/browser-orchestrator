#!/bin/bash
# Configure browser-use main service

echo "Configuring browser-use main service..."

# Check if browser-use is installed
if ! pip show browser-use &> /dev/null; then
    echo "Warning: browser-use not installed. Install with: pip install browser-use"
fi

# Set environment
export BROWSER_USE_MODEL=${BROWSER_USE_MODEL:-MiniMax-Text-01}
export BROWSER_USE_MAX_STEPS=${BROWSER_USE_MAX_STEPS:-12}
export BROWSER_USE_TIMEOUT_SECONDS=${BROWSER_USE_TIMEOUT_SECONDS:-90}
export FALLBACK_MODE=true

echo "browser-use model: $BROWSER_USE_MODEL"
echo "browser-use max steps: $BROWSER_USE_MAX_STEPS"
echo "browser-use timeout: $BROWSER_USE_TIMEOUT_SECONDS"
echo "Main browser-use configuration ready"

# browser-use runs in-process inside the app.
# This script exists only as a configuration helper.

# Keep script running
echo "browser-use helper running. Press Ctrl+C to stop."
tail -f /dev/null
