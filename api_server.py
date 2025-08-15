from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json

app = FastAPI()

# Add CORS middleware for Lovable frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Lovable domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def call_mcp_tool(tool_name: str, **kwargs):
    """Call an MCP tool by running the server as a subprocess"""
    try:
        # Prepare the MCP request
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": kwargs
            }
        }
        
        # Run the MCP server and send the request
        process = subprocess.Popen(
            ["python", "/Users/prerna/MCP-1/sever.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send initialization request first
        init_request = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "api-client", "version": "1.0.0"}
            }
        }
        
        stdout, stderr = process.communicate(
            json.dumps(init_request) + "\n" + json.dumps(request) + "\n"
        )
        
        if process.returncode == 0:
            lines = stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    try:
                        response = json.loads(line)
                        if response.get("id") == 1:  # Our tool call response
                            return response.get("result", {})
                    except json.JSONDecodeError:
                        continue
        
        return {"error": f"Failed to call tool: {stderr}"}
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/collect_requirements")
def collect_requirements(project_name: str, project_type: str, complexity: str, tech_stack: str = "not specified", deadline_weeks: int = 4):
    """Collect requirements and return implementation plan"""
    return call_mcp_tool(
        "collect_requirements",
        project_name=project_name,
        project_type=project_type,
        complexity=complexity,
        tech_stack=tech_stack,
        deadline_weeks=deadline_weeks
    )

@app.get("/provide_base_template")
def provide_base_template(use_case: str):
    """Get base prompt templates for a use case"""
    return call_mcp_tool("provide_base_template", use_case=use_case)

@app.get("/provide_advanced_template")
def provide_advanced_template(base_template: str, style: str = "clean_code"):
    """Enhance a base template with advanced details"""
    return call_mcp_tool("provide_advanced_template", base_template=base_template, style=style)

@app.get("/analyze_process_automation")
def analyze_process_automation(
    process_name: str, 
    primary_goal: str, 
    trigger_type: str, 
    trigger_details: str, 
    success_outcome: str,
    current_steps: str = "not specified",
    stakeholders: str = "not specified", 
    frequency: str = "not specified",
    pain_points: str = "not specified"
):
    """Analyze process automation with detailed recommendations"""
    return call_mcp_tool(
        "analyze_process_automation",
        process_name=process_name,
        primary_goal=primary_goal,
        trigger_type=trigger_type,
        trigger_details=trigger_details,
        success_outcome=success_outcome,
        current_steps=current_steps,
        stakeholders=stakeholders,
        frequency=frequency,
        pain_points=pain_points
    )

@app.get("/")
def root():
    return {"message": "Prompt Context Server API", "endpoints": ["/collect_requirements", "/provide_base_template", "/provide_advanced_template", "/analyze_process_automation"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
