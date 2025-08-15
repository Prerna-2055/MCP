#!/bin/bash

echo "🚀 Firebase Function - Text Plan Generator (Fixed)"
echo "=================================================="

# Check if project parameters are provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <project_name> <project_type> <complexity> [tech_stack]"
    echo ""
    echo "Examples:"
    echo "  $0 \"My E-commerce Store\" ecommerce medium \"React, Node.js, CouchBase\""
    echo "  $0 \"Mobile App\" mobile high \"React Native, Firebase\""
    echo "  $0 \"ML Pipeline\" ml enterprise \"Python, TensorFlow, Kafka\""
    echo ""
    echo "Available project types: webapp, api, mobile, desktop, ml, cli, service, ecommerce, cms, dashboard, game, iot, blockchain, social"
    echo "Available complexity: simple, medium, high, enterprise"
    exit 1
fi

PROJECT_NAME="$1"
PROJECT_TYPE="$2"
COMPLEXITY="$3"
TECH_STACK="${4:-React, Node.js, MongoDB}"

# Create filename
FILENAME="${PROJECT_NAME// /_}_Project_Plan.txt"
FILENAME="${FILENAME//[^a-zA-Z0-9._-]/}"

echo "📋 Generating plan for: $PROJECT_NAME"
echo "🎯 Project Type: $PROJECT_TYPE"
echo "🔧 Complexity: $COMPLEXITY"
echo "💻 Tech Stack: $TECH_STACK"
echo ""

# Make API call and extract response
echo "🌐 Calling Firebase function..."
RESPONSE=$(curl -s -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \
  -H "Content-Type: application/json" \
  -d "{
    \"project_name\": \"$PROJECT_NAME\",
    \"project_type\": \"$PROJECT_TYPE\",
    \"complexity\": \"$COMPLEXITY\",
    \"tech_stack\": \"$TECH_STACK\",
    \"deadline_weeks\": 8,
    \"user_id\": \"bash-script-user\"
  }")

# Check if response is valid JSON
if echo "$RESPONSE" | jq . > /dev/null 2>&1; then
    echo "✅ SUCCESS! Function responded successfully"
    
    # Extract project data
    PROJECT_NAME_RESP=$(echo "$RESPONSE" | jq -r '.project_name')
    PROJECT_TYPE_RESP=$(echo "$RESPONSE" | jq -r '.project_type | ascii_upcase')
    COMPLEXITY_RESP=$(echo "$RESPONSE" | jq -r '.complexity | ascii_upcase')
    TECH_STACK_RESP=$(echo "$RESPONSE" | jq -r '.tech_stack')
    TIMELINE=$(echo "$RESPONSE" | jq -r '.complexity_details.timeline')
    TEAM_SIZE=$(echo "$RESPONSE" | jq -r '.complexity_details.team_size')
    ARCHITECTURE=$(echo "$RESPONSE" | jq -r '.suggested_architecture')
    MIN_COST=$(echo "$RESPONSE" | jq -r '.estimated_cost_range.min')
    MAX_COST=$(echo "$RESPONSE" | jq -r '.estimated_cost_range.max')
    CURRENCY=$(echo "$RESPONSE" | jq -r '.estimated_cost_range.currency')
    
    # Extract phases as simple list
    PHASES=$(echo "$RESPONSE" | jq -r '.phases[]')
    
    # Generate phases section
    PHASES_SECTION=""
    PHASE_NUM=1
    while IFS= read -r phase; do
        if [ ! -z "$phase" ]; then
            PHASES_SECTION+="PHASE $PHASE_NUM: $phase"$'\n'
            PHASES_SECTION+="--------------------------------------------------"$'\n'
            PHASES_SECTION+="Duration: 2 weeks"$'\n'
            PHASES_SECTION+="Key Activities:"$'\n'
            PHASES_SECTION+="• Detailed planning and requirement analysis"$'\n'
            PHASES_SECTION+="• Design and architecture documentation"$'\n'
            PHASES_SECTION+="• Implementation with code reviews"$'\n'
            PHASES_SECTION+="• Testing and quality assurance"$'\n'
            PHASES_SECTION+="• Documentation and knowledge transfer"$'\n'
            PHASES_SECTION+=""$'\n'
            ((PHASE_NUM++))
        fi
    done <<< "$PHASES"
    
    # Generate comprehensive text plan
    cat > "$FILENAME" << EOF
================================================================================
                        PROJECT DEVELOPMENT PLAN & GUIDELINES
================================================================================

Project Name: $PROJECT_NAME_RESP
Project Type: $PROJECT_TYPE_RESP
Complexity Level: $COMPLEXITY_RESP
Generated Date: $(date +"%m/%d/%Y")
Estimated Timeline: $TIMELINE
Budget Range: \$$(printf "%'d" $MIN_COST) - \$$(printf "%'d" $MAX_COST) $CURRENCY

================================================================================
                                EXECUTIVE SUMMARY
================================================================================

This document provides comprehensive guidelines and a detailed implementation plan 
for the $PROJECT_NAME_RESP project. The project is classified as a $COMPLEXITY_RESP 
complexity $PROJECT_TYPE_RESP application using $TECH_STACK_RESP technology stack.

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
$ARCHITECTURE

Technology Stack:
$TECH_STACK_RESP

Key Architectural Principles:
• Scalability: Design for future growth and increased load
• Maintainability: Write clean, documented, and testable code
• Security: Implement security best practices from day one
• Performance: Optimize for speed and efficiency
• Reliability: Build robust error handling and recovery mechanisms

================================================================================
                              DEVELOPMENT PHASES
================================================================================

$PHASES_SECTION

================================================================================
                                TEAM STRUCTURE
================================================================================

Recommended Team Size: $TEAM_SIZE

Team Composition:
$(echo "$RESPONSE" | jq -r '.recommended_team_structure[] | "• \(.)"')

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
$(echo "$RESPONSE" | jq -r '.risks[] | "• \(.)"')

Risk Mitigation Strategies:
• Conduct regular risk assessment meetings
• Implement comprehensive testing at all levels
• Maintain clear communication channels
• Create detailed documentation and knowledge sharing
• Establish backup plans for critical components
• Monitor project progress against milestones

================================================================================
                              COMPLIANCE & SECURITY
================================================================================

GDPR Compliance Requirements:
• Data Protection Impact Assessment (DPIA)
• Privacy by Design implementation
• User consent management system
• Data subject rights implementation (access, rectification, erasure)
• Data breach notification procedures
• Regular compliance audits and documentation
• Staff training on data protection principles
• Third-party processor agreements

Security Standards:
• Implement end-to-end encryption for sensitive data
• Regular security audits and penetration testing
• Multi-factor authentication for admin access
• Secure API design with proper authentication
• Regular security updates and patch management

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
                              SUCCESS METRICS
================================================================================

Technical Metrics:
• Code quality score (>8/10)
• Test coverage (>80%)
• Performance benchmarks met
• Security vulnerabilities (0 critical, <5 medium)
• Documentation completeness (100%)
• GDPR compliance score (100%)

Business Metrics:
• On-time delivery
• Budget adherence
• Stakeholder satisfaction
• User adoption rate
• System uptime and reliability
• GDPR compliance audit results

Compliance Metrics:
• Data protection compliance score
• Privacy policy completeness
• User consent rate
• Data breach response time
• Staff training completion rate

================================================================================
                              COMMUNICATION PLAN
================================================================================

Regular Meetings:
• Daily standups (15 minutes)
• Weekly progress reviews (1 hour)
• Bi-weekly stakeholder updates (30 minutes)
• Monthly retrospectives (1 hour)
• Quarterly compliance reviews (2 hours)

Reporting:
• Weekly status reports
• Monthly budget and timeline updates
• Risk assessment reports
• Quality metrics dashboard
• GDPR compliance reports

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
• GDPR compliance validation

================================================================================
                              MAINTENANCE PLAN
================================================================================

Post-Launch Activities:
• Monitor system performance and user feedback
• Regular security updates and patches
• Feature enhancements based on user needs
• Performance optimization and scaling
• Documentation updates and team training
• GDPR compliance monitoring and updates

Long-term Support:
• Quarterly system health checks
• Annual technology stack reviews
• Continuous improvement implementation
• Knowledge transfer and team development
• Annual GDPR compliance audits

================================================================================
                                  CONCLUSION
================================================================================

This comprehensive plan provides the foundation for successful delivery of the
$PROJECT_NAME_RESP project. Following these guidelines will ensure high-quality
deliverables, efficient team collaboration, and successful project outcomes.

Key Success Factors:
• Adherence to the defined timeline and milestones
• Consistent application of quality standards
• Proactive risk management and mitigation
• Regular communication and stakeholder engagement
• Continuous monitoring and improvement
• Full GDPR compliance implementation

For questions or clarifications, please contact the project team lead.

================================================================================
                              END OF DOCUMENT
================================================================================
EOF

    echo "📄 Text plan generated: $FILENAME"
    echo "📊 File size: $(wc -c < "$FILENAME") bytes"
    echo ""
    echo "📖 Plan Preview (first 10 lines):"
    echo "=================================="
    head -10 "$FILENAME"
    echo "..."
    echo "[Complete plan saved to $FILENAME]"
    
else
    echo "❌ ERROR: Invalid response from Firebase function"
    echo "Response: $RESPONSE"
fi

echo ""
echo "🎯 Usage Examples:"
echo "=================="
echo "./generate_text_plan_fixed.sh \"CouchBase Store\" ecommerce medium \"React, Node.js, CouchBase\""
echo "./generate_text_plan_fixed.sh \"Mobile App\" mobile high \"React Native, Firebase\""
echo "./generate_text_plan_fixed.sh \"ML Pipeline\" ml enterprise \"Python, TensorFlow\""
