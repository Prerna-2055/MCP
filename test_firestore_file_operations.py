#!/usr/bin/env python3
"""
Test script for Firestore file operations
Demonstrates how to create queries, save files, and access them from Firestore
"""

import requests
import json
import time
from datetime import datetime

# Firebase Functions base URL - replace with your actual project URL
BASE_URL = "https://us-central1-mcptest-468919.cloudfunctions.net"

def test_save_text_file():
    """Test saving a text file to Firestore"""
    print("🔥 Testing: Save Text File to Firestore")
    
    url = f"{BASE_URL}/saveTextFile"
    
    # Sample file content
    file_content = """# My Project Notes

This is a sample text file saved directly to Firestore.

## Features:
- Direct storage in Firestore documents
- Searchable by tags and metadata
- User-specific access control
- Download functionality

Created: {datetime.now().isoformat()}
""".format(datetime=datetime)
    
    payload = {
        "filename": "project_notes.txt",
        "content": file_content,
        "user_id": "test_user_123",
        "tags": ["notes", "project", "test"],
        "is_public": False,
        "metadata": {
            "description": "Sample project notes for testing",
            "category": "documentation",
            "version": "1.0"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ File saved successfully!")
        print(f"   File ID: {result['id']}")
        print(f"   Filename: {result['filename']}")
        print(f"   Size: {result['size']} bytes")
        print(f"   Download URL: {result['download_url']}")
        
        return result['id']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saving file: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return None

def test_list_user_files(user_id):
    """Test listing user files"""
    print(f"\n🔍 Testing: List Files for User {user_id}")
    
    url = f"{BASE_URL}/listUserFiles"
    params = {
        "user_id": user_id,
        "limit": 10,
        "page": 0
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Found {result['total']} files")
        
        for file_info in result['files']:
            print(f"   📄 {file_info['filename']}")
            print(f"      ID: {file_info['id']}")
            print(f"      Size: {file_info['size']} bytes")
            print(f"      Tags: {file_info.get('tags', [])}")
            print(f"      Created: {file_info.get('created_at', 'N/A')}")
            print(f"      Download: {file_info['download_url']}")
            print()
        
        return result['files']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error listing files: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return []

def test_download_file(file_id, filename):
    """Test downloading a file from Firestore"""
    print(f"\n⬇️ Testing: Download File {filename}")
    
    url = f"{BASE_URL}/downloadFile"
    params = {"file_id": file_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Save the downloaded content
        download_filename = f"downloaded_{filename}"
        with open(download_filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✅ File downloaded successfully!")
        print(f"   Saved as: {download_filename}")
        print(f"   Content length: {len(response.text)} characters")
        
        # Show first few lines of content
        lines = response.text.split('\n')[:5]
        print(f"   Preview:")
        for line in lines:
            print(f"      {line}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading file: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return False

def test_search_files(user_id, tags=None):
    """Test searching files by tags"""
    print(f"\n🔎 Testing: Search Files by Tags {tags}")
    
    url = f"{BASE_URL}/searchFiles"
    params = {
        "user_id": user_id,
        "limit": 10
    }
    
    if tags:
        params["tags"] = ",".join(tags)
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Search found {result['total']} files")
        
        for file_info in result['files']:
            print(f"   📄 {file_info['filename']}")
            print(f"      Tags: {file_info.get('tags', [])}")
            print(f"      Metadata: {file_info.get('metadata', {})}")
            print()
        
        return result['files']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error searching files: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return []

def test_bulk_save_files():
    """Test bulk saving multiple files"""
    print("\n📦 Testing: Bulk Save Multiple Files")
    
    url = f"{BASE_URL}/bulkSaveFiles"
    
    files_to_save = [
        {
            "filename": "config.txt",
            "content": "# Configuration File\napi_key=test123\ndebug=true",
            "tags": ["config", "settings"],
            "metadata": {"type": "configuration"}
        },
        {
            "filename": "readme.md",
            "content": "# Project README\n\nThis is a test project for Firestore file operations.",
            "tags": ["documentation", "readme"],
            "metadata": {"type": "documentation"}
        },
        {
            "filename": "data.json",
            "content": '{"users": [{"id": 1, "name": "Test User"}]}',
            "content_type": "application/json",
            "tags": ["data", "json"],
            "metadata": {"type": "data"}
        }
    ]
    
    payload = {
        "files": files_to_save,
        "user_id": "test_user_123"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Bulk save successful!")
        print(f"   Files saved: {result['total']}")
        
        for file_info in result['files']:
            print(f"   📄 {file_info['filename']}")
            print(f"      ID: {file_info['id']}")
            print(f"      Size: {file_info['size']} bytes")
        
        return result['files']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error bulk saving files: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return []

def test_save_project_plan():
    """Test saving a project plan (existing functionality)"""
    print("\n📋 Testing: Save Project Plan with File Storage")
    
    url = f"{BASE_URL}/collectRequirements"
    
    payload = {
        "project_name": "E-commerce Platform",
        "project_type": "webapp",
        "complexity": "high",
        "tech_stack": "React + Node.js + PostgreSQL",
        "deadline_weeks": 16,
        "user_id": "test_user_123"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Project plan created successfully!")
        print(f"   Project ID: {result['id']}")
        print(f"   Project Name: {result['project_name']}")
        print(f"   Complexity: {result['complexity']}")
        print(f"   Estimated Cost: ${result['estimated_cost_range']['min']:,} - ${result['estimated_cost_range']['max']:,}")
        print(f"   Timeline: {result['complexity_details']['timeline']}")
        print(f"   Team Size: {result['complexity_details']['team_size']}")
        
        return result['id']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating project plan: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return None

def test_get_file_info(file_id):
    """Test getting file metadata without content"""
    print(f"\n📊 Testing: Get File Info for {file_id}")
    
    url = f"{BASE_URL}/getFileInfo"
    params = {"file_id": file_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ File info retrieved successfully!")
        print(f"   Filename: {result['filename']}")
        print(f"   Size: {result['size']} bytes")
        print(f"   Content Type: {result['content_type']}")
        print(f"   Tags: {result.get('tags', [])}")
        print(f"   Public: {result.get('is_public', False)}")
        print(f"   Metadata: {json.dumps(result.get('metadata', {}), indent=2)}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting file info: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return None

def main():
    """Run all tests"""
    print("🚀 Starting Firestore File Operations Tests")
    print("=" * 50)
    
    user_id = "test_user_123"
    
    # Test 1: Save a single text file
    file_id = test_save_text_file()
    
    if file_id:
        # Test 2: Get file info
        test_get_file_info(file_id)
        
        # Test 3: Download the file
        test_download_file(file_id, "project_notes.txt")
    
    # Test 4: Bulk save multiple files
    bulk_files = test_bulk_save_files()
    
    # Test 5: List all user files
    user_files = test_list_user_files(user_id)
    
    # Test 6: Search files by tags
    test_search_files(user_id, ["notes", "project"])
    
    # Test 7: Save project plan (existing functionality)
    project_id = test_save_project_plan()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n📝 Summary:")
    print(f"   - Files can be saved directly to Firestore documents")
    print(f"   - Files are searchable by tags, user, and metadata")
    print(f"   - Files can be downloaded via direct URLs")
    print(f"   - Bulk operations are supported for efficiency")
    print(f"   - Integration with existing project plan functionality")
    
    print("\n🔗 Next Steps:")
    print(f"   1. Deploy your Firebase Functions: firebase deploy --only functions")
    print(f"   2. Update security rules for production use")
    print(f"   3. Integrate with your frontend application")
    print(f"   4. Add authentication for user-specific access")

if __name__ == "__main__":
    main()
