#!/bin/bash

# MCP Tools Testing Script with cURL Commands
# This script tests all available MCP tools through the FastAPI server

echo "=== MCP Tools Testing with cURL ==="
echo "Starting API server in background..."

# Start the API server in background
python api_server.py &
API_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Test if server is running
echo "Testing server availability..."
curl -s http://localhost:8000/ | jq '.' || echo "Server not responding or jq not installed"

echo ""
echo "=== Testing collect_requirements tool ==="
echo "Test 1: Basic ecommerce project"
curl -s "http://localhost:8000/collect_requirements?project_name=Test%20Store&project_type=ecommerce&complexity=medium&tech_stack=React%2C%20Node.js&deadline_weeks=8" | jq '.' || echo "Request failed"

echo ""
echo "Test 2: Simple web application"
curl -s "http://localhost:8000/collect_requirements?project_name=Simple%20App&project_type=web%20application&complexity=simple" | jq '.' || echo "Request failed"

echo ""
echo "Test 3: Complex enterprise system"
curl -s "http://localhost:8000/collect_requirements?project_name=Enterprise%20System&project_type=enterprise&complexity=high&tech_stack=Java%2C%20Spring%2C%20PostgreSQL&deadline_weeks=16" | jq '.' || echo "Request failed"

echo ""
echo "=== Testing provide_base_template tool ==="
echo "Test 1: Web application template"
curl -s "http://localhost:8000/provide_base_template?use_case=web%20application" | jq '.' || echo "Request failed"

echo ""
echo "Test 2: Ecommerce template"
curl -s "http://localhost:8000/provide_base_template?use_case=ecommerce" | jq '.' || echo "Request failed"

echo ""
echo "Test 3: API template"
curl -s "http://localhost:8000/provide_base_template?use_case=api" | jq '.' || echo "Request failed"

echo ""
echo "=== Testing provide_advanced_template tool ==="
echo "Test 1: Clean code style"
curl -s "http://localhost:8000/provide_advanced_template?base_template=Basic%20web%20app&style=clean_code" | jq '.' || echo "Request failed"

echo ""
echo "Test 2: Enterprise style"
curl -s "http://localhost:8000/provide_advanced_template?base_template=REST%20API&style=enterprise" | jq '.' || echo "Request failed"

echo ""
echo "=== Testing analyze_process_automation tool ==="
echo "Test 1: Order processing automation"
curl -s -G "http://localhost:8000/analyze_process_automation" \
  --data-urlencode "process_name=Order Processing" \
  --data-urlencode "primary_goal=Automate order fulfillment" \
  --data-urlencode "trigger_type=event" \
  --data-urlencode "trigger_details=New order received" \
  --data-urlencode "success_outcome=Order shipped automatically" \
  --data-urlencode "current_steps=Manual review and processing" \
  --data-urlencode "stakeholders=Sales team, warehouse staff" \
  --data-urlencode "frequency=50 orders per day" \
  --data-urlencode "pain_points=Manual delays, human errors" | jq '.' || echo "Request failed"

echo ""
echo "Test 2: Customer support automation"
curl -s -G "http://localhost:8000/analyze_process_automation" \
  --data-urlencode "process_name=Customer Support Tickets" \
  --data-urlencode "primary_goal=Auto-categorize and route tickets" \
  --data-urlencode "trigger_type=form_submission" \
  --data-urlencode "trigger_details=Support ticket submitted" \
  --data-urlencode "success_outcome=Ticket routed to correct department" | jq '.' || echo "Request failed"

echo ""
echo "=== Testing Error Handling ==="
echo "Test 1: Invalid project type"
curl -s "http://localhost:8000/collect_requirements?project_name=Test&project_type=invalid&complexity=medium" | jq '.' || echo "Request failed"

echo ""
echo "Test 2: Missing required parameters"
curl -s "http://localhost:8000/collect_requirements?project_name=Test" | jq '.' || echo "Request failed"

echo ""
echo "=== Performance Testing ==="
echo "Test 1: Multiple concurrent requests"
for i in {1..3}; do
  curl -s "http://localhost:8000/collect_requirements?project_name=Concurrent%20Test%20$i&project_type=web%20application&complexity=simple" | jq '.project_name' &
done
wait

echo ""
echo "=== Testing Complete ==="
echo "Stopping API server..."
kill $API_PID 2>/dev/null

echo "All tests completed!"
echo ""
echo "=== Summary of Available Endpoints ==="
echo "1. GET /collect_requirements - Collect project requirements and generate implementation plan"
echo "2. GET /provide_base_template - Get base prompt templates for specific use cases"
echo "3. GET /provide_advanced_template - Enhance base templates with advanced details"
echo "4. GET /analyze_process_automation - Analyze and provide automation recommendations"
echo ""
echo "=== Example cURL Commands ==="
echo ""
echo "# Basic requirements collection:"
echo 'curl "http://localhost:8000/collect_requirements?project_name=My%20Store&project_type=ecommerce&complexity=medium"'
echo ""
echo "# Get base template:"
echo 'curl "http://localhost:8000/provide_base_template?use_case=web%20application"'
echo ""
echo "# Process automation analysis:"
echo 'curl -G "http://localhost:8000/analyze_process_automation" \'
echo '  --data-urlencode "process_name=Order Processing" \'
echo '  --data-urlencode "primary_goal=Automate fulfillment" \'
echo '  --data-urlencode "trigger_type=event" \'
echo '  --data-urlencode "trigger_details=New order" \'
echo '  --data-urlencode "success_outcome=Auto-shipped"'
