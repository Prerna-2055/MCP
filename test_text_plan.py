import requests
import json

# Test the Firebase function with text plan output
url = "https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements"

# Test data for CouchBase e-commerce project
test_data = {
    "project_name": "CouchBase E-commerce Store",
    "project_type": "ecommerce",
    "complexity": "medium",
    "tech_stack": "React, Node.js, CouchBase, Redis",
    "deadline_weeks": 8,
    "user_id": "ecommerce-user-1"
}

print("🚀 Testing Firebase Function - Text Plan Generation")
print("=" * 60)
print(f"URL: {url}")
print(f"Request Data: {json.dumps(test_data, indent=2)}")
print("\n" + "=" * 60)

try:
    response = requests.post(url, json=test_data, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Function returned comprehensive plan!")
        
        # Extract the text plan
        text_plan = result.get('text_plan', '')
        plan_filename = result.get('plan_filename', 'project_plan.txt')
        
        print(f"\n📄 Generated Plan File: {plan_filename}")
        print(f"📋 Plan Length: {len(text_plan)} characters")
        
        # Save the text plan to a file
        with open(plan_filename, 'w', encoding='utf-8') as f:
            f.write(text_plan)
        
        print(f"✅ Text plan saved to: {plan_filename}")
        
        # Display first few lines of the plan
        print("\n📖 Plan Preview (first 10 lines):")
        print("-" * 40)
        lines = text_plan.split('\n')[:10]
        for line in lines:
            print(line)
        print("...")
        print(f"[Full plan saved to {plan_filename}]")
        
        # Display key metadata
        print(f"\n📊 Project Metadata:")
        print(f"• Project: {result.get('project_name', 'N/A')}")
        print(f"• Type: {result.get('project_type', 'N/A')}")
        print(f"• Complexity: {result.get('complexity', 'N/A')}")
        print(f"• Tech Stack: {result.get('tech_stack', 'N/A')}")
        print(f"• Timeline: {result.get('complexity_details', {}).get('timeline', 'N/A')}")
        
        cost_range = result.get('estimated_cost_range', {})
        print(f"• Budget: ${cost_range.get('min', 0):,} - ${cost_range.get('max', 0):,}")
        
        team = result.get('recommended_team_structure', [])
        print(f"• Team: {', '.join(team[:3])}{'...' if len(team) > 3 else ''}")
        
    else:
        print(f"❌ ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ REQUEST ERROR: {e}")
except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {e}")

print("\n" + "=" * 60)
print("🎯 CURL Command to generate text plan:")
print("-" * 30)
print('curl -X POST \\')
print('  https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \\')
print('  -H "Content-Type: application/json" \\')
print('  -d \'{"project_name": "My Project", "project_type": "webapp", "complexity": "medium", "tech_stack": "React, Node.js, CouchBase"}\'')
print("\n💡 The response will include a 'text_plan' field with comprehensive guidelines!")
