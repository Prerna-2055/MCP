import requests
import json

# Test the Firebase function with CouchBase
url = "https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements"

# Test data with CouchBase instead of MongoDB
test_data = {
    "project_name": "CouchBase Web App",
    "project_type": "webapp",
    "complexity": "medium",
    "tech_stack": "React, Node.js, CouchBase",
    "deadline_weeks": 8,
    "user_id": "couchbase-user-456"
}

print("Testing Firebase Function with CouchBase...")
print(f"URL: {url}")
print(f"Data: {json.dumps(test_data, indent=2)}")
print("\n" + "="*50)

try:
    # Test POST request
    response = requests.post(url, json=test_data, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS: Function accepts CouchBase tech stack!")
        result = response.json()
        print(f"Document ID: {result.get('id', 'N/A')}")
        print(f"Project Name: {result.get('project_name', 'N/A')}")
        print(f"Tech Stack: {result.get('tech_stack', 'N/A')}")
        print(f"Suggested Architecture: {result.get('suggested_architecture', 'N/A')}")
        print(f"Implementation Phases: {result.get('phases', [])}")
    else:
        print(f"\n❌ ERROR: Function returned status {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ REQUEST ERROR: {e}")
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")

print("\n" + "="*50)
print("CURL Command for CouchBase:")
print('curl -X POST \\')
print('  https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \\')
print('  -H "Content-Type: application/json" \\')
print("  -d '{")
print('    "project_name": "CouchBase Web App",')
print('    "project_type": "webapp",')
print('    "complexity": "medium",')
print('    "tech_stack": "React, Node.js, CouchBase",')
print('    "deadline_weeks": 8,')
print('    "user_id": "couchbase-user-456"')
print("  }'")
