#!/bin/bash
# Health Check Script

echo "Running Browser Orchestrator Health Check..."
echo ""

# Check orchestrator
echo "Checking Orchestrator..."
HEALTH=$(curl -s http://localhost:3101/health)
if [ $? -eq 0 ]; then
    echo "✅ Orchestrator: OK"
    echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
else
    echo "❌ Orchestrator: FAILED"
    echo "Is the orchestrator running? (python3 adapter/app.py)"
    exit 1
fi

echo ""

# Check tools endpoint
echo "Checking Tools Endpoint..."
TOOLS=$(curl -s http://localhost:3101/mcp/tools)
if [ $? -eq 0 ]; then
    echo "✅ Tools: OK"
    TOOL_COUNT=$(echo "$TOOLS" | grep -o '"name"' | wc -l)
    echo "   Available tools: $TOOL_COUNT"
else
    echo "❌ Tools: FAILED"
fi

echo ""
echo "========================================="
echo "Health check complete"
echo "========================================="
