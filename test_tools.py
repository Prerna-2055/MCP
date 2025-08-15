#!/usr/bin/env python3
"""
Test script for the Prompt Context Server tools
Usage: python test_tools.py
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_collect_requirements():
    print("=== Testing collect_requirements ===")
    
    # Example 1: Web Application
    params = {
        "project_name": "TaskManager",
        "project_type": "webapp",
        "complexity": "medium",
        "tech_stack": "React + Node.js",
        "deadline_weeks": 4
    }
    
    response = requests.get(f"{API_BASE}/collect_requirements", params=params)
    print(f"Request: {response.url}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_base_templates():
    print("=== Testing provide_base_template ===")
    
    use_cases = ["webapp", "api", "ml", "cli"]
    
    for use_case in use_cases:
        params = {"use_case": use_case}
        response = requests.get(f"{API_BASE}/provide_base_template", params=params)
        print(f"Use case: {use_case}")
        print(f"Templates: {json.dumps(response.json(), indent=2)}")
        print()

def test_advanced_templates():
    print("=== Testing provide_advanced_template ===")
    
    examples = [
        {
            "base_template": "Create a user authentication system",
            "style": "security_first"
        },
        {
            "base_template": "Build a REST API for inventory management",
            "style": "performance"
        },
        {
            "base_template": "Design a responsive dashboard",
            "style": "clean_code"
        }
    ]
    
    for example in examples:
        response = requests.get(f"{API_BASE}/provide_advanced_template", params=example)
        print(f"Base template: {example['base_template']}")
        print(f"Style: {example['style']}")
        print(f"Enhanced template: {response.text}")
        print()

def interactive_test():
    print("=== Interactive Testing ===")
    print("Enter your own inputs to test the tools:")
    
    # Collect requirements
    print("\n1. Collect Requirements:")
    project_name = input("Project name: ") or "MyProject"
    project_type = input("Project type (webapp/api/ml/cli/service): ") or "webapp"
    complexity = input("Complexity (low/medium/high): ") or "medium"
    tech_stack = input("Tech stack: ") or "not specified"
    deadline_weeks = input("Deadline in weeks: ") or "4"
    
    params = {
        "project_name": project_name,
        "project_type": project_type,
        "complexity": complexity,
        "tech_stack": tech_stack,
        "deadline_weeks": int(deadline_weeks)
    }
    
    response = requests.get(f"{API_BASE}/collect_requirements", params=params)
    print(f"\nResult: {json.dumps(response.json(), indent=2)}")
    
    # Base template
    print("\n2. Get Base Template:")
    use_case = input("Use case (webapp/api/ml/cli): ") or "webapp"
    
    params = {"use_case": use_case}
    response = requests.get(f"{API_BASE}/provide_base_template", params=params)
    templates = response.json()
    print(f"\nBase templates: {json.dumps(templates, indent=2)}")
    
    # Advanced template
    if templates:
        print("\n3. Enhance Template:")
        base_template = input("Enter a template or description: ") or templates[0] if isinstance(templates, list) else str(templates)
        style = input("Style (clean_code/security_first/performance): ") or "clean_code"
        
        params = {
            "base_template": base_template,
            "style": style
        }
        
        response = requests.get(f"{API_BASE}/provide_advanced_template", params=params)
        print(f"\nEnhanced template: {response.text}")

if __name__ == "__main__":
    try:
        # Test if API server is running
        response = requests.get(f"{API_BASE}/")
        print("API Server is running!")
        print(f"Available endpoints: {response.json()['endpoints']}")
        print()
        
        # Run example tests
        test_collect_requirements()
        test_base_templates()
        test_advanced_templates()
        
        # Interactive testing
        interactive_test()
        
    except requests.exceptions.ConnectionError:
        print("Error: API server is not running!")
        print("Please start the server with: python api_server.py")
    except Exception as e:
        print(f"Error: {e}")
