# How to Use Firebase MCP Tool to Create .cline Rules

## 🚀 Quick Start Guide

Here's exactly how to use the Firebase download MCP tool to create .cline rules from your Firebase app:

## Method 1: Using MCP Tools (Recommended)

### Step 1: Restart Cline/MCP Server
The MCP server needs to be restarted to recognize the new tools. You can do this by:
1. Restarting Cline
2. Or asking me to restart the MCP connection

### Step 2: Use the MCP Tool
Once the server is restarted, you can use the tool like this:

```
Download a Firebase text file and convert it to .cline rules using the download_firebase_txt_file tool with these parameters:
- firebase_url: "https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan"
- filename: "My_Project_Plan.txt"
- save_as_cline_rules: true
- cline_rules_filename: "My_Project_rules.txt"
```

### Step 3: Check the Results
The tool will create two files:
- `My_Project_Plan.txt` - Original downloaded file
- `My_Project_rules.txt` - Converted .cline rules file

## Method 2: Direct Command (Works Now)

### Option A: Use the Standalone Script
```bash
python firebase_download_standalone.py
```

This will automatically:
1. Download sample files from Firebase
2. Convert them to .cline rules format
3. Save both original and .cline rules versions

### Option B: Custom Download
Create a simple Python script:

```python
from firebase_download_standalone import download_firebase_txt_file

# Download and convert a specific file
result = download_firebase_txt_file(
    firebase_url="https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan",
    filename="GDPR_Compliance_Project.txt",
    save_as_cline_rules=True,
    cline_rules_filename="GDPR_Compliance_rules.txt"
)

print(f"Success: {result['success']}")
if result['success']:
    print(f"Original file: {result['original_file']}")
    print(f"Cline rules file: {result['cline_rules_file']}")
```

## 📋 What You Get

### Original File (e.g., `My_Project_Plan.txt`)
```
PROJECT DEVELOPMENT PLAN & GUIDELINES

Project Name: My Project
Project Type: WEBAPP
Complexity Level: MEDIUM
...
[Full project plan content]
```

### .cline Rules File (e.g., `My_Project_rules.txt`)
```
create_template

Create a new template for my project project generation.

Arguments

````json
{
  "input": {
    "name": "My Project",
    "description": "Comprehensive project template generated from Firebase download",
    "category": "project_template",
    "template_content": "[Escaped project plan content]",
    "variables": [
      {
        "name": "project_name",
        "type": "string",
        "description": "Name of the project",
        "required": true
      },
      {
        "name": "developer_name", 
        "type": "string",
        "description": "Name of the lead developer",
        "required": true
      }
      // ... more variables
    ],
    "validation_rules": [
      {
        "name": "project_validation",
        "rule_type": "compliance",
        "compliance_type": "project_standards"
      }
    ],
    "author": "Firebase Download System",
    "tags": ["project-template", "firebase", "automated"],
    "source_file": "My_Project_Plan.txt",
    "download_timestamp": "2025-08-14T16:41:00.000000"
  }
}
````
```

## 🎯 Practical Examples

### Example 1: Download GDPR Compliance Template
```python
result = download_firebase_txt_file(
    firebase_url="downloadTextPlan",  # Short form - will construct full URL
    filename="GDPR_Compliance_Template.txt",
    save_as_cline_rules=True
)
```

### Example 2: Download E-commerce Project Plan
```python
result = download_firebase_txt_file(
    firebase_url="https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan",
    filename="Ecommerce_Store_Plan.txt",
    save_as_cline_rules=True,
    cline_rules_filename="Ecommerce_Store_rules.txt"
)
```

### Example 3: List Available Files First
```python
from firebase_download_standalone import list_firebase_files

# See what's available
files = list_firebase_files()
print(f"Found {files['files_count']} files:")
for file_info in files['files']:
    print(f"- {file_info['project_name']} ({file_info['project_type']})")
```

## 🔧 Using the .cline Rules

Once you have the .cline rules file, you can use it with Cline:

### 1. Save as .cline Rules
The generated file is already in the correct format. Just ensure it has the right content structure.

### 2. Use with Cline
You can then tell Cline:
```
Use the template from My_Project_rules.txt to create a new project
```

### 3. Customize Variables
The .cline rules include variables like:
- `project_name` - Name of your project
- `developer_name` - Your name
- `organization` - Your organization
- `tech_stack` - Technology stack to use
- `complexity` - Project complexity level

## 🚨 Troubleshooting

### If MCP Tools Don't Work
1. **Restart Cline** - The MCP server needs to restart to see new tools
2. **Use Standalone Script** - Run `python firebase_download_standalone.py`
3. **Check Server Status** - Ensure the MCP server is running

### If Download Fails
1. **Check Internet Connection**
2. **Verify Firebase URL** - Make sure the Firebase function is deployed
3. **Try Different Parameters** - Use different project names or complexity levels

### If .cline Rules Format is Wrong
The tool automatically creates proper format, but you can:
1. **Check the generated file** - Look at `Sample_Firebase_rules.txt` for reference
2. **Modify variables** - Edit the JSON structure as needed
3. **Test with Cline** - Try using the rules file with Cline

## 📁 File Locations

All files are created in your current directory (`/Users/prerna/MCP-1/`):
- Original downloads: `[filename].txt`
- .cline rules: `[filename]_rules.txt`

## 🎉 Ready-to-Use Examples

I've already created these working examples for you:
- `Sample_Firebase_rules.txt` - Sample project template
- `Custom_GDPR_Project_rules.txt` - GDPR compliance template

You can use these immediately with Cline or as templates for creating your own!

## 💡 Pro Tips

1. **Use Descriptive Filenames** - Makes it easier to find your templates later
2. **Customize Variables** - Edit the generated .cline rules to add project-specific variables
3. **Test First** - Use the standalone script to test before using MCP tools
4. **Keep Originals** - The tool preserves both original and converted files
5. **Check Firebase Functions** - Ensure your Firebase functions are deployed and accessible

---

**Ready to use right now!** Try running `python firebase_download_standalone.py` to see it in action.
