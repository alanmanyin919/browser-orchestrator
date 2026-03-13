#!/bin/bash
# Start All Services

echo "========================================="
echo "Starting Browser Orchestrator Stack"
echo "========================================="

# Create logs directory
mkdir -p logs

# Load environment
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Function to cleanup on exit
cleanup() {
    echo "Stopping services..."
    kill $PRIMARY_PID $FALLBACK_PID $ORCH_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Main backend config (browser-use)
echo "[1/3] Preparing browser-use..."
./scripts/start_fallback.sh &
FALLBACK_PID=$!

# Wait a bit
sleep 2

# Start Secondary backend config (Playwright)
echo "[2/3] Preparing Playwright MCP..."
./scripts/start_primary.sh &
PRIMARY_PID=$!

# Wait a bit
sleep 2

# Start Orchestrator
echo "[3/3] Starting Orchestrator..."
python3 adapter/app.py &
ORCH_PID=$!

echo ""
echo "========================================="
echo "All services started!"
echo "========================================="
echo "Orchestrator: http://localhost:3101"
echo "Health:       http://localhost:3101/health"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for all processes
wait
