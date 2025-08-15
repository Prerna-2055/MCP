import requests
import json

# Test the enhanced Firebase function with multiple options
url = "https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements"

# Test different project types and complexity levels
test_cases = [
    {
        "name": "Simple E-commerce Project",
        "data": {
            "project_name": "Online Store",
            "project_type": "ecommerce",
            "complexity": "simple",
            "tech_stack": "React, Node.js, CouchBase",
            "deadline_weeks": 4,
            "user_id": "ecommerce-user-1"
        }
    },
    {
        "name": "Enterprise Mobile App",
        "data": {
            "project_name": "Corporate Mobile App",
            "project_type": "mobile",
            "complexity": "enterprise",
            "tech_stack": "React Native, Node.js, PostgreSQL",
            "deadline_weeks": 20,
            "user_id": "mobile-user-1"
        }
    },
    {
        "name": "High Complexity ML Project",
        "data": {
            "project_name": "AI Recommendation Engine",
            "project_type": "ml",
            "complexity": "high",
            "tech_stack": "Python, TensorFlow, Apache Kafka, Redis",
            "deadline_weeks": 16,
            "user_id": "ml-user-1"
        }
    },
    {
        "name": "Medium Complexity Dashboard",
        "data": {
            "project_name": "Analytics Dashboard",
            "project_type": "dashboard",
            "complexity": "medium",
            "tech_stack": "Vue.js, Express, InfluxDB",
            "deadline_weeks": 8,
            "user_id": "dashboard-user-1"
        }
    },
    {
        "name": "Simple IoT Project",
        "data": {
            "project_name": "Smart Home System",
            "project_type": "iot",
            "complexity": "simple",
            "tech_stack": "Arduino, MQTT, Node.js, MongoDB",
            "deadline_weeks": 6,
            "user_id": "iot-user-1"
        }
    }
]

print("🚀 Testing Enhanced Firebase Function with Multiple Options")
print("=" * 60)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n📋 Test Case {i}: {test_case['name']}")
    print("-" * 40)
    
    try:
        response = requests.post(url, json=test_case['data'], timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS")
            print(f"📊 Project Type: {result.get('project_type', 'N/A')}")
            print(f"🔧 Complexity: {result.get('complexity', 'N/A')}")
            print(f"🏗️  Architecture: {result.get('suggested_architecture', 'N/A')}")
            
            # Display complexity details
            complexity_details = result.get('complexity_details', {})
            print(f"⏱️  Timeline: {complexity_details.get('timeline', 'N/A')}")
            print(f"👥 Team Size: {complexity_details.get('team_size', 'N/A')}")
            
            # Display cost estimate
            cost_range = result.get('estimated_cost_range', {})
            print(f"💰 Cost Range: ${cost_range.get('min', 0):,} - ${cost_range.get('max', 0):,} {cost_range.get('currency', 'USD')}")
            
            # Display team structure
            team_structure = result.get('recommended_team_structure', [])
            print(f"🏢 Team Structure: {', '.join(team_structure[:3])}{'...' if len(team_structure) > 3 else ''}")
            
            # Display phases
            phases = result.get('phases', [])
            print(f"📈 Key Phases: {len(phases)} phases defined")
            
            # Display risks
            risks = result.get('risks', [])
            print(f"⚠️  Key Risks: {', '.join(risks[:2])}{'...' if len(risks) > 2 else ''}")
            
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

print("\n" + "=" * 60)
print("📋 AVAILABLE OPTIONS SUMMARY:")
print("=" * 60)

print("\n🎯 PROJECT TYPES:")
project_types = [
    "webapp", "api", "mobile", "desktop", "ml", "cli", "service", 
    "ecommerce", "cms", "dashboard", "game", "iot", "blockchain", "social"
]
for pt in project_types:
    print(f"  • {pt}")

print("\n📊 COMPLEXITY LEVELS:")
complexity_levels = ["simple", "medium", "high", "enterprise"]
for cl in complexity_levels:
    print(f"  • {cl}")

print("\n💡 EXAMPLE CURL COMMANDS:")
print("-" * 30)

print("\n# E-commerce Project:")
print('curl -X POST \\')
print('  https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \\')
print('  -H "Content-Type: application/json" \\')
print('  -d \'{"project_name": "Online Store", "project_type": "ecommerce", "complexity": "medium", "tech_stack": "React, Node.js, CouchBase"}\'')

print("\n# Mobile App Project:")
print('curl -X POST \\')
print('  https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \\')
print('  -H "Content-Type: application/json" \\')
print('  -d \'{"project_name": "Mobile App", "project_type": "mobile", "complexity": "high", "tech_stack": "React Native, Firebase"}\'')

print("\n# IoT Project:")
print('curl -X POST \\')
print('  https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \\')
print('  -H "Content-Type: application/json" \\')
print('  -d \'{"project_name": "Smart Home", "project_type": "iot", "complexity": "simple", "tech_stack": "Arduino, MQTT, Node.js"}\'')
