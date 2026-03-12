#!/bin/bash
# Start Better Browser Use Fallback Service

echo "Starting Better Browser Use Fallback Service..."

# Check if browser-use is installed
if ! pip show browser-use &> /dev/null; then
    echo "Warning: browser-use not installed. Install with: pip install browser-use"
fi

# Set environment
export BROWSER_USE_API_URL=${BROWSER_USE_API_URL:-http://localhost:8000}
export FALLBACK_MODE=true

echo "Better Browser Use URL: $BROWSER_USE_API_URL"
echo "Fallback service ready"

# In production, would start actual browser-use server here
# For now, this is a placeholder

# Keep script running
echo "Fallback service running. Press Ctrl+C to stop."
tail -f /dev/null
