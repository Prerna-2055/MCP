# Firebase Download MCP Tool Guide

## Overview

The Firebase Download MCP Tool provides functionality to download .txt files from Firebase applications and automatically convert them to .cline rules format. This tool is integrated into the existing MCP server and provides two main capabilities:

1. **Download Firebase Text Files** - Download .txt files from Firebase Cloud Functions or Storage
2. **Convert to .cline Rules** - Automatically convert downloaded content to .cline rules template format
3. **List Firebase Files** - Browse available files in Firebase Firestore collections

## Features

### 🔥 Firebase Integration
- Connect to Firebase Cloud Functions
- Download text files from Firebase Storage
- Query Firestore collections for available files
- Support for custom Firebase project IDs

### 📄 File Download & Conversion
- Download .txt files from Firebase URLs
- Automatic conversion to .cline rules format
- Preserve original files alongside converted versions
- Support for custom filenames and paths

### 🔧 .cline Rules Generation
- Automatic template creation with proper JSON structure
- Variable definitions for project customization
- Validation rules for compliance checking
- Metadata tracking (source file, timestamp, author)

## Available MCP Tools

### 1. `download_firebase_txt_file`

Downloads a .txt file from Firebase and optionally converts it to .cline rules format.

**Parameters:**
- `firebase_url` (required): Firebase function URL or direct file URL
- `project_id` (optional): Firebase project ID (default: "mcptest-468919")
- `file_path` (optional): Path in Firebase storage or collection name
- `filename` (optional): Specific filename to download
- `save_as_cline_rules` (optional): Whether to save as .cline rules format (default: true)
- `cline_rules_filename` (optional): Custom filename for .cline rules

**Example Usage:**
```json
{
  "firebase_url": "https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan",
  "filename": "My_Project_Plan.txt",
  "save_as_cline_rules": true,
  "cline_rules_filename": "My_Project_rules.txt"
}
```

### 2. `list_firebase_files`

Lists available files/documents in Firebase that can be downloaded.

**Parameters:**
- `project_id` (optional): Firebase project ID (default: "mcptest-468919")
- `collection` (optional): Firestore collection name to query (default: "project_requirements")
- `limit` (optional): Maximum number of files to return (default: 10)

**Example Usage:**
```json
{
  "project_id": "mcptest-468919",
  "collection": "project_requirements",
  "limit": 5
}
```

## Installation & Setup

### 1. MCP Server Configuration

The Firebase download tools are already integrated into the existing MCP server (`sever.py`). The server is configured in your MCP settings at:

```
/Users/prerna/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

Current configuration:
```json
{
  "mcpServers": {
    "prompt-context-server": {
      "timeout": 60,
      "command": "python",
      "args": ["/Users/prerna/MCP-1/sever.py"],
      "env": {},
      "type": "stdio"
    }
  }
}
```

### 2. Dependencies

Required Python packages (already installed):
- `requests` - For HTTP requests to Firebase
- `fastmcp` - MCP server framework
- `json` - JSON handling
- `datetime` - Timestamp generation

## Usage Examples

### Example 1: Download and Convert Firebase Project Plan

```python
# Using the MCP tool
result = download_firebase_txt_file(
    firebase_url="https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan",
    filename="GDPR_Compliance_Project.txt",
    save_as_cline_rules=True
)

# Result:
{
  "success": True,
  "original_file": "GDPR_Compliance_Project.txt",
  "file_size": 15420,
  "cline_rules_file": "GDPR_Compliance_Project_rules.txt",
  "cline_rules_created": True,
  "download_url": "https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan",
  "timestamp": "2025-08-14T16:36:43.612649"
}
```

### Example 2: List Available Firebase Files

```python
# Using the MCP tool
result = list_firebase_files(
    project_id="mcptest-468919",
    collection="project_requirements",
    limit=5
)

# Result:
{
  "success": True,
  "files_count": 3,
  "files": [
    {
      "document_id": "abc123",
      "project_name": "E-commerce Platform",
      "project_type": "webapp",
      "complexity": "high",
      "created_at": "2025-08-14T10:30:00Z",
      "download_url": "https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan"
    }
  ]
}
```

### Example 3: Custom Firebase Project

```python
# Download from custom Firebase project
result = download_firebase_txt_file(
    firebase_url="downloadTextPlan",  # Will construct full URL
    project_id="my-custom-project",
    filename="Custom_App_Plan.txt",
    save_as_cline_rules=True
)
```

## .cline Rules Format

The tool automatically converts downloaded content to .cline rules format with the following structure:

```
create_template

Create a new template for [project name] project generation.

Arguments

````json
{
  "input": {
    "name": "[Project Name]",
    "description": "Comprehensive project template generated from Firebase download",
    "category": "project_template",
    "template_content": "[Escaped original content]",
    "variables": [
      {
        "name": "project_name",
        "type": "string",
        "description": "Name of the project",
        "required": true
      },
      // ... more variables
    ],
    "validation_rules": [
      {
        "name": "project_validation",
        "rule_type": "compliance",
        "compliance_type": "project_standards",
        "parameters": {
          "standards_type": "enterprise"
        },
        "error_message": "Project standards compliance requirements not met"
      }
    ],
    "author": "Firebase Download System",
    "tags": ["project-template", "firebase", "automated", "enterprise"],
    "source_file": "[original filename]",
    "download_timestamp": "[ISO timestamp]"
  }
}
````
```

## Testing

### Standalone Testing

A standalone test script is available for testing the functionality:

```bash
python firebase_download_standalone.py
```

This will:
1. List available Firebase files
2. Download a sample text plan
3. Convert it to .cline rules format
4. Test custom parameter handling

### Test Results

The test successfully creates:
- `Sample_Firebase_Project_Plan.txt` - Original downloaded file
- `Sample_Firebase_rules.txt` - Converted .cline rules file
- `Custom_GDPR_Project.txt` - Custom download test
- `Custom_GDPR_Project_rules.txt` - Custom .cline rules

## Firebase Project Configuration

### Current Firebase Setup

- **Project ID**: `mcptest-468919`
- **Region**: `us-central1`
- **Functions**: Available at `https://us-central1-mcptest-468919.cloudfunctions.net/`
- **Firestore**: Collections include `project_requirements`, `template_requests`, etc.

### Available Firebase Functions

1. **downloadTextPlan** - Downloads project plans as text files
2. **collectRequirements** - Collects project requirements
3. **getUserProjects** - Gets user project history
4. **analyzeProcessAutomation** - Process automation analysis

## Error Handling

The tool includes comprehensive error handling:

### Network Errors
```json
{
  "success": false,
  "error": "Network error: Connection timeout",
  "firebase_url": "https://..."
}
```

### Firebase API Errors
```json
{
  "success": false,
  "error": "Firebase API error: 404",
  "message": "Function not found"
}
```

### File System Errors
```json
{
  "success": false,
  "error": "Unexpected error: Permission denied",
  "firebase_url": "https://..."
}
```

## Best Practices

### 1. File Naming
- Use descriptive filenames that indicate the project type
- Include version numbers or dates for tracking
- Follow consistent naming conventions

### 2. .cline Rules
- Review generated .cline rules before use
- Customize variables based on specific project needs
- Add additional validation rules as required

### 3. Firebase URLs
- Use full URLs for external Firebase projects
- Use function names for the default project
- Include necessary parameters for Firebase functions

### 4. Error Handling
- Always check the `success` field in responses
- Log errors for debugging
- Implement retry logic for network issues

## Troubleshooting

### Common Issues

1. **"Network error: Connection timeout"**
   - Check internet connection
   - Verify Firebase function is deployed and running
   - Check Firebase project permissions

2. **"Firebase API error: 403"**
   - Verify Firebase project permissions
   - Check if authentication is required
   - Ensure proper API keys are configured

3. **"File not found" errors**
   - Verify the Firebase function exists
   - Check the project ID is correct
   - Ensure the function is deployed

### Debug Mode

For debugging, you can modify the standalone test script to include more verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Integration with Cline

The downloaded .cline rules files can be used directly with Cline for:

1. **Project Template Generation** - Use as templates for new projects
2. **Code Generation** - Generate code based on project plans
3. **Compliance Checking** - Validate projects against standards
4. **Documentation** - Create project documentation

## Future Enhancements

Potential improvements for the Firebase download tool:

1. **Authentication Support** - Add Firebase Auth integration
2. **Batch Downloads** - Download multiple files at once
3. **File Filtering** - Filter files by type, date, or project
4. **Custom Templates** - Support for custom .cline rules templates
5. **Webhook Integration** - Automatic downloads on Firebase updates

## Support

For issues or questions about the Firebase Download MCP Tool:

1. Check the error messages and troubleshooting guide
2. Review the Firebase project configuration
3. Test with the standalone script first
4. Check MCP server logs for detailed error information

---

**Created**: August 14, 2025  
**Version**: 1.0  
**Author**: Firebase Download System  
**Last Updated**: August 14, 2025
