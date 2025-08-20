#!/bin/bash

echo "=== Simple cURL Test for MCP Tools ==="
echo ""

# Start API server in background
echo "Starting API server..."
python api_server.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo "Testing server health check..."
curl -s http://localhost:8000/ | python -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))"

echo ""
echo "Testing collect_requirements tool..."
curl -s "http://localhost:8000/collect_requirements?project_name=Demo%20Store&project_type=ecommerce&complexity=simple&tech_stack=React" | python -c "import sys, json; data=sys.stdin.read(); print('Response:', data if data.strip() else 'Empty response')"

echo ""
echo "Stopping server..."
kill $SERVER_PID 2>/dev/null

echo ""
echo "=== Direct MCP Tool Test (Working Alternative) ==="
echo "Since the API server has communication issues, here's the working MCP tool output:"
echo ""
