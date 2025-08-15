import requests
import json

# Extract text plan from the current Firebase function response
url = "https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements"

def generate_text_plan(project_data):
    """Generate a comprehensive text plan from project data"""
    
    current_date = "8/14/2025"
    project_name = project_data.get('project_name', 'Unknown Project')
    project_type = project_data.get('project_type', 'webapp').upper()
    complexity = project_data.get('complexity', 'medium').upper()
    tech_stack = project_data.get('tech_stack', 'Not specified')
    deadline_weeks = project_data.get('deadline_weeks', 4)
    
    complexity_details = project_data.get('complexity_details', {})
    timeline = complexity_details.get('timeline', '1-3 months')
    team_size = complexity_details.get('team_size', '2-4 developers')
    
    cost_range = project_data.get('estimated_cost_range', {})
    min_cost = cost_range.get('min', 0)
    max_cost = cost_range.get('max', 0)
    currency = cost_range.get('currency', 'USD')
    
    suggested_architecture = project_data.get('suggested_architecture', 'General architecture')
    phases = project_data.get('phases', [])
    risks = project_data.get('risks', [])
    team_structure = project_data.get('recommended_team_structure', [])
    
    text_plan = f"""
================================================================================
                        PROJECT DEVELOPMENT PLAN & GUIDELINES
================================================================================

Project Name: {project_name}
Project Type: {project_type}
Complexity Level: {complexity}
Generated Date: {current_date}
Estimated Timeline: {timeline}
Budget Range: ${min_cost:,} - ${max_cost:,} {currency}

================================================================================
                                EXECUTIVE SUMMARY
================================================================================

This document provides comprehensive guidelines and a detailed implementation plan 
for the {project_name} project. The project is classified as a {complexity.lower()} 
complexity {project_type.lower()} application using {tech_stack} technology stack.

Key Success Factors:
• Clear project scope and requirements definition
• Proper team structure and role allocation
• Risk mitigation strategies implementation
• Adherence to best practices and coding standards
• Regular progress monitoring and quality assurance

================================================================================
                              TECHNICAL ARCHITECTURE
================================================================================

Recommended Architecture:
{suggested_architecture}

Technology Stack:
{tech_stack}

Key Architectural Principles:
• Scalability: Design for future growth and increased load
• Maintainability: Write clean, documented, and testable code
• Security: Implement security best practices from day one
• Performance: Optimize for speed and efficiency
• Reliability: Build robust error handling and recovery mechanisms

================================================================================
                              DEVELOPMENT PHASES
================================================================================

{chr(10).join([f"PHASE {i+1}: {phase}" + chr(10) + "-" * 50 + chr(10) + f"Duration: {deadline_weeks // len(phases)} weeks" + chr(10) + "Key Activities:" + chr(10) + "• Detailed planning and requirement analysis" + chr(10) + "• Design and architecture documentation" + chr(10) + "• Implementation with code reviews" + chr(10) + "• Testing and quality assurance" + chr(10) + "• Documentation and knowledge transfer" for i, phase in enumerate(phases)])}

================================================================================
                                TEAM STRUCTURE
================================================================================

Recommended Team Size: {team_size}

Team Composition:
{chr(10).join([f"• {role}" for role in team_structure])}

Team Responsibilities:
• Project Manager: Overall coordination, timeline management, stakeholder communication
• Lead Developer: Technical leadership, architecture decisions, code reviews
• Developers: Feature implementation, unit testing, documentation
• UI/UX Designer: User interface design, user experience optimization
• QA Tester: Test planning, execution, bug reporting and tracking
• DevOps Engineer: Infrastructure setup, deployment automation, monitoring

================================================================================
                                RISK ASSESSMENT
================================================================================

Identified Risks:
{chr(10).join([f"• {risk}" for risk in risks])}

Risk Mitigation Strategies:
• Conduct regular risk assessment meetings
• Implement comprehensive testing at all levels
• Maintain clear communication channels
• Create detailed documentation and knowledge sharing
• Establish backup plans for critical components
• Monitor project progress against milestones

================================================================================
                              QUALITY GUIDELINES
================================================================================

Code Quality Standards:
• Follow language-specific coding conventions
• Implement comprehensive unit and integration tests
• Maintain minimum 80% code coverage
• Conduct peer code reviews for all changes
• Use automated linting and formatting tools
• Document all public APIs and complex logic

Testing Strategy:
• Unit Testing: Test individual components and functions
• Integration Testing: Test component interactions
• System Testing: Test complete system functionality
• User Acceptance Testing: Validate against requirements
• Performance Testing: Ensure scalability and speed
• Security Testing: Identify and fix vulnerabilities

================================================================================
                              PROJECT MILESTONES
================================================================================

Week 1-2: Project Setup & Planning
• Team onboarding and role assignment
• Development environment setup
• Project structure and repository creation
• Initial architecture documentation

Week 3-{deadline_weeks // 2}: Core Development
• Implement core functionality
• Set up basic infrastructure
• Create initial user interfaces
• Establish testing framework

Week {deadline_weeks // 2 + 1}-{int(deadline_weeks * 0.8)}: Feature Development
• Implement advanced features
• Integration with external services
• Performance optimization
• Security implementation

Week {int(deadline_weeks * 0.8) + 1}-{deadline_weeks}: Testing & Deployment
• Comprehensive testing and bug fixes
• Performance tuning and optimization
• Production deployment preparation
• Documentation completion and handover

================================================================================
                              SUCCESS METRICS
================================================================================

Technical Metrics:
• Code quality score (>8/10)
• Test coverage (>80%)
• Performance benchmarks met
• Security vulnerabilities (0 critical, <5 medium)
• Documentation completeness (100%)

Business Metrics:
• On-time delivery
• Budget adherence
• Stakeholder satisfaction
• User adoption rate
• System uptime and reliability

================================================================================
                              COMMUNICATION PLAN
================================================================================

Regular Meetings:
• Daily standups (15 minutes)
• Weekly progress reviews (1 hour)
• Bi-weekly stakeholder updates (30 minutes)
• Monthly retrospectives (1 hour)

Reporting:
• Weekly status reports
• Monthly budget and timeline updates
• Risk assessment reports
• Quality metrics dashboard

================================================================================
                              DEPLOYMENT STRATEGY
================================================================================

Environment Strategy:
• Development: Local development and unit testing
• Staging: Integration testing and user acceptance testing
• Production: Live system with monitoring and backup

Deployment Process:
• Automated CI/CD pipeline
• Blue-green deployment for zero downtime
• Rollback procedures for quick recovery
• Monitoring and alerting setup
• Performance and security monitoring

================================================================================
                                  CONCLUSION
================================================================================

This comprehensive plan provides the foundation for successful delivery of the
{project_name} project. Following these guidelines will ensure high-quality
deliverables, efficient team collaboration, and successful project outcomes.

Key Success Factors:
• Adherence to the defined timeline and milestones
• Consistent application of quality standards
• Proactive risk management and mitigation
• Regular communication and stakeholder engagement
• Continuous monitoring and improvement

For questions or clarifications, please contact the project team lead.

================================================================================
                              END OF DOCUMENT
================================================================================
""".strip()
    
    return text_plan

# Test the function and generate text plan
test_data = {
    "project_name": "CouchBase E-commerce Store",
    "project_type": "ecommerce",
    "complexity": "medium",
    "tech_stack": "React, Node.js, CouchBase, Redis",
    "deadline_weeks": 8,
    "user_id": "test-user"
}

print("🚀 Generating Text Plan from Firebase Function Response")
print("=" * 60)

try:
    response = requests.post(url, json=test_data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Generating text plan...")
        
        # Generate text plan from response
        text_plan = generate_text_plan(result)
        filename = f"{result['project_name'].replace(' ', '_')}_Project_Plan.txt"
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_plan)
        
        print(f"📄 Text plan saved to: {filename}")
        print(f"📋 Plan length: {len(text_plan)} characters")
        
        # Show preview
        print(f"\n📖 Plan Preview:")
        print("-" * 40)
        lines = text_plan.split('\n')[:15]
        for line in lines:
            print(line)
        print("...")
        print(f"[Complete plan saved to {filename}]")
        
    else:
        print(f"❌ ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

print(f"\n🎯 To download text plan:")
print("1. Run this script: python extract_text_plan.py")
print("2. Or use the curl command and pipe to jq to extract text_plan field")
print("3. The function generates comprehensive project guidelines as text!")
