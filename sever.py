from fastmcp import FastMCP, tools
import requests
import os
import json
from datetime import datetime

# Create the FastMCP app
app = FastMCP("prompt-context-server")

# ---------------------------
# Tool 1: Collect Requirements → Implementation Plan
# ---------------------------
@app.tool
def collect_requirements(
    project_name: str,
    project_type: str,   # api, webapp, ml, cli, service
    complexity: str,     # low, medium, high
    tech_stack: str = "not specified",
    deadline_weeks: int = 4
) -> dict:
    """
    Collects generic requirements and returns an implementation plan.
    """
    suggested_arch = {
        "api": "REST or GraphQL service with modular monolith design",
        "webapp": "SPA with component-based architecture",
        "ml": "ML pipeline with model registry & feature store",
        "cli": "Command-line tool with modular commands",
        "service": "Microservice or serverless function design"
    }.get(project_type, "General layered architecture")

    return {
        "project_name": project_name,
        "project_type": project_type,
        "complexity": complexity,
        "tech_stack": tech_stack,
        "deadline_weeks": deadline_weeks,
        "suggested_architecture": suggested_arch,
        "phases": [
            "Requirement gathering & scoping",
            "Architecture & design",
            "Implementation & testing",
            "Deployment & monitoring"
        ],
        "risks": [
            "Scope creep",
            "Tight deadlines",
            "Integration challenges"
        ]
    }

# ---------------------------
# Tool 2: Provide Base Prompt Template
# ---------------------------
@app.tool
def provide_base_template(use_case: str) -> list:
    """
    Returns base prompt templates for a given use case.
    """
    templates = {
        "api": [
            "Design REST endpoints for {feature}. Include OpenAPI spec.",
            "Generate CRUD API with authentication for {feature}."
        ],
        "webapp": [
            "Plan UI components for {feature} with responsive design.",
            "Create a React component hierarchy for {feature}."
        ],
        "ml": [
            "Design ML pipeline for {objective}, including preprocessing steps.",
            "Suggest model architecture for {objective}."
        ]
    }
    return templates.get(use_case.lower(), ["No templates available for this use case."])

# ---------------------------
# Tool 3: Provide Advanced Prompt Template
# ---------------------------
@app.tool
def provide_advanced_template(base_template: str, style: str = "clean_code") -> str:
    """
    Enhances a base template with advanced details.
    """
    enhancements = {
        "clean_code": "- Follow clean code principles.\n- Add comments and docstrings.",
        "security_first": "- Include security best practices.\n- Validate all inputs.",
        "performance": "- Optimize for low latency.\n- Add caching where possible."
    }
    extra = enhancements.get(style, "- General improvements applied.")
    return f"{base_template}\n\nAdditional Guidance:\n{extra}"

# ---------------------------
# Tool 4: Advanced Process Automation Analysis
# ---------------------------
@app.tool
def analyze_process_automation(
    process_name: str,
    primary_goal: str,  # save_time, reduce_errors, improve_compliance, enhance_visibility, standardize_process
    trigger_type: str,  # email, form_submission, system_record, schedule, manual
    trigger_details: str,
    success_outcome: str,
    current_steps: str = "not specified",
    stakeholders: str = "not specified",
    frequency: str = "not specified",
    pain_points: str = "not specified"
) -> dict:
    """
    Provides detailed process automation analysis with comprehensive recommendations.
    """
    
    # Goal-specific recommendations
    goal_strategies = {
        "save_time": {
            "focus": "Time optimization and parallel processing",
            "metrics": ["Time saved per execution", "Processing speed improvement", "Manual hours reduced"],
            "recommendations": [
                "Implement parallel processing where possible",
                "Use batch operations for bulk tasks",
                "Cache frequently accessed data",
                "Automate repetitive decision points"
            ]
        },
        "reduce_errors": {
            "focus": "Error prevention and validation",
            "metrics": ["Error rate reduction", "Data accuracy improvement", "Exception handling coverage"],
            "recommendations": [
                "Add comprehensive input validation",
                "Implement data quality checks",
                "Create error handling workflows",
                "Add confirmation steps for critical actions"
            ]
        },
        "improve_compliance": {
            "focus": "Audit trails and regulatory adherence",
            "metrics": ["Audit trail completeness", "Compliance score", "Documentation coverage"],
            "recommendations": [
                "Log all process steps with timestamps",
                "Implement approval workflows",
                "Create compliance checkpoints",
                "Generate audit reports automatically"
            ]
        },
        "enhance_visibility": {
            "focus": "Monitoring and reporting",
            "metrics": ["Process visibility score", "Reporting accuracy", "Real-time monitoring coverage"],
            "recommendations": [
                "Create real-time dashboards",
                "Implement status notifications",
                "Add progress tracking",
                "Generate automated reports"
            ]
        },
        "standardize_process": {
            "focus": "Consistency and best practices",
            "metrics": ["Process consistency score", "Standard adherence rate", "Variation reduction"],
            "recommendations": [
                "Define clear process templates",
                "Implement standard workflows",
                "Add quality gates",
                "Create process documentation"
            ]
        }
    }
    
    # Trigger-specific implementation details
    trigger_implementations = {
        "email": {
            "setup": "Email monitoring with filters and parsing",
            "considerations": ["Email parsing accuracy", "Attachment handling", "Spam filtering"],
            "tools": ["Email APIs", "Natural language processing", "File parsers"]
        },
        "form_submission": {
            "setup": "Webhook integration with form platforms",
            "considerations": ["Data validation", "Form field mapping", "Error handling"],
            "tools": ["Webhook handlers", "Form APIs", "Data validators"]
        },
        "system_record": {
            "setup": "Database triggers or API webhooks",
            "considerations": ["Real-time vs batch processing", "Data consistency", "System integration"],
            "tools": ["Database triggers", "API integrations", "Event streaming"]
        },
        "schedule": {
            "setup": "Cron jobs or scheduled tasks",
            "considerations": ["Timing optimization", "Resource availability", "Failure recovery"],
            "tools": ["Task schedulers", "Monitoring systems", "Retry mechanisms"]
        },
        "manual": {
            "setup": "User interface with trigger buttons",
            "considerations": ["User permissions", "Input validation", "Progress feedback"],
            "tools": ["Web interfaces", "Mobile apps", "Notification systems"]
        }
    }
    
    selected_goal = goal_strategies.get(primary_goal, goal_strategies["save_time"])
    selected_trigger = trigger_implementations.get(trigger_type, trigger_implementations["manual"])
    
    # Generate detailed analysis
    analysis = {
        "process_overview": {
            "name": process_name,
            "primary_goal": primary_goal,
            "focus_area": selected_goal["focus"],
            "trigger_type": trigger_type,
            "trigger_details": trigger_details,
            "success_criteria": success_outcome
        },
        "automation_strategy": {
            "key_recommendations": selected_goal["recommendations"],
            "success_metrics": selected_goal["metrics"],
            "implementation_approach": selected_trigger["setup"],
            "technical_considerations": selected_trigger["considerations"],
            "recommended_tools": selected_trigger["tools"]
        },
        "detailed_implementation": {
            "phase_1_discovery": [
                "Map current process flow in detail",
                "Identify all stakeholders and their roles",
                "Document current pain points and bottlenecks",
                "Analyze data flow and dependencies"
            ],
            "phase_2_design": [
                "Create automated workflow diagram",
                "Define error handling scenarios",
                "Design user interfaces and notifications",
                "Plan integration points with existing systems"
            ],
            "phase_3_development": [
                "Build core automation logic",
                "Implement trigger mechanisms",
                "Create monitoring and logging",
                "Develop user interfaces"
            ],
            "phase_4_testing": [
                "Unit test individual components",
                "Integration test with existing systems",
                "User acceptance testing",
                "Performance and load testing"
            ],
            "phase_5_deployment": [
                "Deploy to production environment",
                "Train users on new process",
                "Monitor initial performance",
                "Gather feedback and iterate"
            ]
        },
        "risk_assessment": {
            "technical_risks": [
                "System integration complexity",
                "Data quality and validation issues",
                "Performance bottlenecks",
                "Security vulnerabilities"
            ],
            "business_risks": [
                "User adoption challenges",
                "Process disruption during transition",
                "Compliance and regulatory issues",
                "Change management resistance"
            ],
            "mitigation_strategies": [
                "Implement comprehensive testing",
                "Create rollback procedures",
                "Provide thorough user training",
                "Establish monitoring and alerting"
            ]
        },
        "success_framework": {
            "kpis": selected_goal["metrics"],
            "monitoring_approach": "Real-time dashboards with automated alerts",
            "review_schedule": "Weekly performance reviews for first month, then monthly",
            "optimization_plan": "Continuous improvement based on user feedback and performance data"
        },
        "next_steps": [
            f"Conduct detailed process mapping session with stakeholders",
            f"Create technical specification document",
            f"Estimate development timeline and resources",
            f"Set up development environment and tools",
            f"Begin Phase 1: Discovery and documentation"
        ]
    }
    
    return analysis

# ---------------------------
# Tool 5: Firebase Text File Download
# ---------------------------
@app.tool
def download_firebase_txt_file(
    firebase_url: str,
    project_id: str = "your-firebase-project-id",
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
    "template_content": "{content.replace('"', '\\"').replace('\n', '\\n')}",
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

# ---------------------------
# Tool 6: List Firebase Files
# ---------------------------
@app.tool
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

# ---------------------------
# Run MCP server
# ---------------------------
if __name__ == "__main__":
    app.run()
