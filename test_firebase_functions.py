#!/usr/bin/env python3
"""
Test script for Firebase Cloud Functions
"""

import requests
import json

# Your Firebase project function URLs
BASE_URL = "https://us-central1-mcptest-468919.cloudfunctions.net"

def test_collect_requirements():
    print("🧪 Testing collectRequirements...")
    
    url = f"{BASE_URL}/collectRequirements"
    data = {
        "project_name": "E-commerce Platform",
        "project_type": "webapp",
        "complexity": "high",
        "tech_stack": "React + Node.js + PostgreSQL",
        "deadline_weeks": 12,
        "user_id": "test-user"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Project: {result.get('project_name')}")
            print(f"Architecture: {result.get('suggested_architecture')}")
            print(f"Firebase ID: {result.get('id')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    print()

def test_base_templates():
    print("🧪 Testing getBaseTemplates...")
    
    url = f"{BASE_URL}/getBaseTemplates"
    data = {
        "use_case": "api",
        "user_id": "test-user"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Templates: {result.get('templates')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    print()

def test_advanced_template():
    print("🧪 Testing getAdvancedTemplate...")
    
    url = f"{BASE_URL}/getAdvancedTemplate"
    data = {
        "base_template": "Design REST endpoints for user management system",
        "style": "security_first",
        "user_id": "test-user"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Enhanced template:")
            print(result.get('enhanced_template'))
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    print()

def test_process_automation():
    print("🧪 Testing analyzeProcessAutomation (Advanced Tool)...")
    
    url = f"{BASE_URL}/analyzeProcessAutomation"
    data = {
        "process_name": "Customer Invoice Approval",
        "primary_goal": "improve_compliance",
        "trigger_type": "email",
        "trigger_details": "Invoice received at invoices@company.com with PDF attachment",
        "success_outcome": "Invoice is approved/rejected with complete audit trail and payment processed",
        "current_steps": "Manual email review, manager approval, accounting entry",
        "stakeholders": "Accounting, Finance Manager, Accounts Payable",
        "frequency": "50-100 invoices per week",
        "pain_points": "Approval delays, missing audit trails, manual data entry errors",
        "user_id": "test-user"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Process: {result.get('process_overview', {}).get('name')}")
            print(f"Focus Area: {result.get('process_overview', {}).get('focus_area')}")
            print(f"Key Recommendations: {len(result.get('automation_strategy', {}).get('key_recommendations', []))} items")
            print(f"Implementation Phases: {len(result.get('detailed_implementation', {}))} phases")
            print(f"Firebase ID: {result.get('id')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    print()

def test_get_user_projects():
    print("🧪 Testing getUserProjects...")
    
    url = f"{BASE_URL}/getUserProjects"
    params = {"user_id": "test-user"}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            projects = result.get('projects', [])
            print(f"✅ Success! Found {len(projects)} projects for user")
            for i, project in enumerate(projects[:3]):  # Show first 3
                print(f"  {i+1}. {project.get('project_name', 'Unknown')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    print()

if __name__ == "__main__":
    print("🔥 Firebase Functions Test Suite")
    print("=" * 50)
    print(f"Testing functions at: {BASE_URL}")
    print()
    
    # Test all functions
    test_collect_requirements()
    test_base_templates()
    test_advanced_template()
    test_process_automation()
    test_get_user_projects()
    
    print("🎉 Testing complete!")
    print()
    print("💡 Tips:")
    print("- If you see 'Method not allowed' errors, make sure you're using POST requests")
    print("- If functions aren't found, check Firebase Console for deployment status")
    print("- Check Firebase Console > Functions > Logs for detailed error messages")
