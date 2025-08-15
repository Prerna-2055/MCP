import requests
import json

# Test the fixed Firebase function
url = "https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements"

# Simple test data
test_data = {
    "project_name": "Test Project",
    "project_type": "webapp",
    "complexity": "simple",
    "tech_stack": "React, Node.js, CouchBase",
    "deadline_weeks": 4,
    "user_id": "test-user"
}

print("🔧 Testing Fixed Firebase Function...")
print(f"URL: {url}")
print(f"Data: {json.dumps(test_data, indent=2)}")
print("\n" + "="*50)

try:
    response = requests.post(url, json=test_data, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Function is working properly!")
        print(f"📋 Project: {result.get('project_name', 'N/A')}")
        print(f"🎯 Type: {result.get('project_type', 'N/A')}")
        print(f"🔧 Complexity: {result.get('complexity', 'N/A')}")
        print(f"🏗️  Architecture: {result.get('suggested_architecture', 'N/A')}")
        
        # Check if enhanced features are working
        if 'complexity_details' in result:
            complexity_details = result['complexity_details']
            print(f"⏱️  Timeline: {complexity_details.get('timeline', 'N/A')}")
            print(f"👥 Team Size: {complexity_details.get('team_size', 'N/A')}")
        
        if 'estimated_cost_range' in result:
            cost_range = result['estimated_cost_range']
            print(f"💰 Cost: ${cost_range.get('min', 0):,} - ${cost_range.get('max', 0):,}")
        
        if 'recommended_team_structure' in result:
            team = result['recommended_team_structure']
            print(f"🏢 Team: {', '.join(team[:3])}")
            
        print(f"📄 Document ID: {result.get('id', 'N/A')}")
        
    else:
        print(f"❌ ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ REQUEST ERROR: {e}")
except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {e}")

print("\n" + "="*50)
print("🎉 If successful, the enhanced function is now working!")
