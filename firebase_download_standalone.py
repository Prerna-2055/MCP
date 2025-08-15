#!/usr/bin/env python3
"""
Standalone Firebase download functions for testing
"""

import requests
import os
import json
from datetime import datetime

def download_firebase_txt_file(
    firebase_url: str,
    project_id: str = "mcptest-468919",
    file_path: str = "project_plans",
    filename: str = "",
    save_as_cline_rules: bool = True,
    cline_rules_filename: str = ""
) -> dict:
    """
    Downloads a .txt file from Firebase and optionally saves it as .cline rules.
    
    Args:
        firebase_url: Firebase function URL or direct file URL
        project_id: Firebase project ID (default: mcptest-468919)
        file_path: Path in Firebase storage or collection name
        filename: Specific filename to download (if empty, will try to extract from URL)
        save_as_cline_rules: Whether to save as .cline rules format
        cline_rules_filename: Custom filename for .cline rules (if empty, auto-generated)
    """
    
    try:
        # Construct Firebase URL if not provided as full URL
        if not firebase_url.startswith('http'):
            base_url = f"https://us-central1-{project_id}.cloudfunctions.net"
            firebase_url = f"{base_url}/{firebase_url}"
        
        # Add parameters for text plan download
        if "downloadTextPlan" in firebase_url:
            params = {
                "project_name": filename.replace("_Project_Plan.txt", "").replace("_", " ") if filename else "Sample Project",
                "project_type": "webapp",
                "complexity": "medium",
                "tech_stack": "React, Node.js, Firebase",
                "deadline_weeks": 8
            }
            
            # Make request to Firebase function
            response = requests.get(firebase_url, params=params)
        else:
            # Direct file download
            response = requests.get(firebase_url)
        
        response.raise_for_status()
        
        # Get the content
        content = response.text
        
        # Determine filename
        if not filename:
            # Try to extract from Content-Disposition header
            content_disposition = response.headers.get('content-disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"')
            else:
                filename = f"downloaded_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Ensure .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Save the original file
        original_path = filename
        with open(original_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        result = {
            "success": True,
            "original_file": original_path,
            "file_size": len(content),
            "download_url": firebase_url,
            "timestamp": datetime.now().isoformat()
        }
        
        # Convert to .cline rules format if requested
        if save_as_cline_rules:
            cline_rules_content = convert_to_cline_rules(content, filename)
            
            # Determine .cline rules filename
            if not cline_rules_filename:
                base_name = filename.replace('.txt', '')
                cline_rules_filename = f"{base_name}_rules.txt"
            
            # Save as .cline rules
            with open(cline_rules_filename, 'w', encoding='utf-8') as f:
                f.write(cline_rules_content)
            
            result.update({
                "cline_rules_file": cline_rules_filename,
                "cline_rules_created": True,
                "cline_rules_size": len(cline_rules_content)
            })
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Network error: {str(e)}",
            "firebase_url": firebase_url
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "firebase_url": firebase_url
        }

def convert_to_cline_rules(content: str, original_filename: str) -> str:
    """
    Converts downloaded content to .cline rules format.
    """
    
    # Extract project name from filename or content
    project_name = original_filename.replace('_Project_Plan.txt', '').replace('_', ' ')
    if 'Project Name:' in content:
        try:
            project_name = content.split('Project Name:')[1].split('\n')[0].strip()
        except:
            pass
    
    # Escape content for JSON
    escaped_content = content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    # Create .cline rules format
    cline_rules = f"""create_template

Create a new template for {project_name.lower()} project generation.

Arguments

````json
{{
  "input": {{
    "name": "{project_name}",
    "description": "Comprehensive project template generated from Firebase download",
    "category": "project_template",
    "template_content": "{escaped_content}",
    "variables": [
      {{
        "name": "project_name",
        "type": "string",
        "description": "Name of the project",
        "required": true
      }},
      {{
        "name": "developer_name", 
        "type": "string",
        "description": "Name of the lead developer",
        "required": true
      }},
      {{
        "name": "organization",
        "type": "string",
        "description": "Organization name",
        "required": true
      }},
      {{
        "name": "project_type",
        "type": "string",
        "description": "Type of project",
        "allowed_values": ["webapp", "api", "mobile", "desktop", "ml", "cli"],
        "required": true
      }},
      {{
        "name": "complexity",
        "type": "string",
        "description": "Project complexity level",
        "allowed_values": ["simple", "medium", "high", "enterprise"],
        "default_value": "medium",
        "required": false
      }},
      {{
        "name": "tech_stack",
        "type": "string",
        "description": "Technology stack to use",
        "required": true
      }},
      {{
        "name": "deadline_weeks",
        "type": "integer",
        "description": "Project deadline in weeks",
        "default_value": 8,
        "required": false
      }},
      {{
        "name": "generation_date",
        "type": "string",
        "description": "Date when template was generated",
        "required": true
      }}
    ],
    "validation_rules": [
      {{
        "name": "project_validation",
        "rule_type": "compliance",
        "compliance_type": "project_standards",
        "parameters": {{
          "standards_type": "enterprise"
        }},
        "error_message": "Project standards compliance requirements not met"
      }}
    ],
    "author": "Firebase Download System",
    "tags": ["project-template", "firebase", "automated", "enterprise"],
    "source_file": "{original_filename}",
    "download_timestamp": "{datetime.now().isoformat()}"
  }}
}}
````"""
    
    return cline_rules

def list_firebase_files(
    project_id: str = "mcptest-468919",
    collection: str = "project_requirements",
    limit: int = 10
) -> dict:
    """
    Lists available files/documents in Firebase that can be downloaded.
    
    Args:
        project_id: Firebase project ID
        collection: Firestore collection name to query
        limit: Maximum number of files to return
    """
    
    try:
        # Construct Firebase REST API URL for Firestore
        base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection}"
        
        # Make request to list documents
        response = requests.get(f"{base_url}?pageSize={limit}")
        
        if response.status_code == 200:
            data = response.json()
            documents = data.get('documents', [])
            
            files_list = []
            for doc in documents:
                doc_id = doc['name'].split('/')[-1]
                fields = doc.get('fields', {})
                
                # Extract relevant information
                file_info = {
                    "document_id": doc_id,
                    "project_name": fields.get('project_name', {}).get('stringValue', 'Unknown'),
                    "project_type": fields.get('project_type', {}).get('stringValue', 'Unknown'),
                    "complexity": fields.get('complexity', {}).get('stringValue', 'Unknown'),
                    "created_at": fields.get('created_at', {}).get('timestampValue', 'Unknown'),
                    "download_url": f"https://us-central1-{project_id}.cloudfunctions.net/downloadTextPlan"
                }
                
                # Add filename if available
                if 'plan_filename' in fields:
                    file_info['filename'] = fields['plan_filename'].get('stringValue', '')
                
                files_list.append(file_info)
            
            return {
                "success": True,
                "files_count": len(files_list),
                "files": files_list,
                "collection": collection,
                "project_id": project_id
            }
        else:
            return {
                "success": False,
                "error": f"Firebase API error: {response.status_code}",
                "message": response.text
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error listing Firebase files: {str(e)}"
        }

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
