#!/usr/bin/env python3
"""
Test script for Firebase download MCP tool functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sever import download_firebase_txt_file, list_firebase_files

def test_firebase_download():
    """Test the Firebase download functionality"""
    
    print("🔥 Testing Firebase Download MCP Tool")
    print("=" * 50)
    
    # Test 1: List available Firebase files
    print("\n📋 Test 1: Listing Firebase files...")
    try:
        result = list_firebase_files()
        print(f"✅ Success: Found {result.get('files_count', 0)} files")
        if result.get('success') and result.get('files'):
            for i, file_info in enumerate(result['files'][:3], 1):  # Show first 3 files
                print(f"   {i}. {file_info.get('project_name', 'Unknown')} ({file_info.get('project_type', 'Unknown')})")
    except Exception as e:
        print(f"❌ Error listing files: {e}")
    
    # Test 2: Download a sample text plan
    print("\n📥 Test 2: Downloading sample text plan...")
    try:
        firebase_url = "https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan"
        result = download_firebase_txt_file(
            firebase_url=firebase_url,
            filename="Sample_Firebase_Project_Plan.txt",
            save_as_cline_rules=True,
            cline_rules_filename="Sample_Firebase_rules.txt"
        )
        
        if result.get('success'):
            print(f"✅ Download successful!")
            print(f"   📄 Original file: {result.get('original_file')}")
            print(f"   📏 File size: {result.get('file_size')} bytes")
            print(f"   🔧 Cline rules file: {result.get('cline_rules_file')}")
            print(f"   📏 Cline rules size: {result.get('cline_rules_size')} bytes")
        else:
            print(f"❌ Download failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
    
    # Test 3: Download with custom parameters
    print("\n📥 Test 3: Downloading with custom parameters...")
    try:
        firebase_url = "downloadTextPlan"  # Test URL construction
        result = download_firebase_txt_file(
            firebase_url=firebase_url,
            project_id="mcptest-468919",
            filename="Custom_GDPR_Project.txt",
            save_as_cline_rules=True
        )
        
        if result.get('success'):
            print(f"✅ Custom download successful!")
            print(f"   📄 Original file: {result.get('original_file')}")
            print(f"   🔧 Cline rules file: {result.get('cline_rules_file')}")
        else:
            print(f"❌ Custom download failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error with custom download: {e}")
    
    print("\n🎉 Firebase Download MCP Tool testing completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_firebase_download()
