import requests
import json

# Test the Firebase function
url = "https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements"

# Test data
test_data = {
    "project_name": "Test Project",
    "project_type": "webapp",
    "complexity": "medium",
    "tech_stack": "React, Node.js, MongoDB",
    "deadline_weeks": 6,
    "user_id": "test-user-123"
}

print("Testing Firebase Function...")
print(f"URL: {url}")
print(f"Data: {json.dumps(test_data, indent=2)}")
print("\n" + "="*50)

try:
    # Test POST request
    response = requests.post(url, json=test_data, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS: Function is working properly!")
        result = response.json()
        print(f"Document ID: {result.get('id', 'N/A')}")
        print(f"Project Name: {result.get('project_name', 'N/A')}")
        print(f"Suggested Architecture: {result.get('suggested_architecture', 'N/A')}")
    else:
        print(f"\n❌ ERROR: Function returned status {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ REQUEST ERROR: {e}")
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")
