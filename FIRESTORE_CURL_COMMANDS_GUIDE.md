# 🔥 Firestore File Operations - Curl Commands Guide
## Complete Reference for Downloading and Managing Files

This guide provides practical curl commands for accessing your Firestore-based file operations and GDPR-compliant e-commerce functions.

## 📋 Table of Contents
1. [Project Plan Downloads](#project-plan-downloads)
2. [GDPR E-commerce Operations](#gdpr-e-commerce-operations)
3. [File Management Operations](#file-management-operations)
4. [Compliance and Audit Operations](#compliance-and-audit-operations)
5. [Batch Operations](#batch-operations)

## 🚀 Project Plan Downloads

### Download Project Plan as Text File

```bash
# Basic project plan download
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "CouchBase Store",
    "project_type": "ecommerce",
    "complexity": "medium",
    "tech_stack": "React, Node.js, CouchBase"
  }' \
  -o "couchbase_store_plan.txt"
```

```bash
# Advanced project plan with custom timeline
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "GDPR E-commerce Platform",
    "project_type": "ecommerce",
    "complexity": "high",
    "tech_stack": "React, Node.js, Firebase, Stripe",
    "deadline_weeks": 16,
    "user_id": "developer_123"
  }' \
  -o "gdpr_ecommerce_plan.txt"
```

```bash
# Mobile app project plan
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Shopping Mobile App",
    "project_type": "mobile",
    "complexity": "high",
    "tech_stack": "React Native, Firebase, Redux",
    "deadline_weeks": 20
  }' \
  -o "mobile_shopping_app_plan.txt"
```

### Create and Store Project Requirements

```bash
# Create project requirements (stored in Firestore)
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Sustainable Fashion Store",
    "project_type": "ecommerce",
    "complexity": "medium",
    "tech_stack": "Next.js, Stripe, PostgreSQL",
    "deadline_weeks": 12,
    "user_id": "client_456"
  }'
```

## 🛒 GDPR E-commerce Operations

### User Registration with GDPR Compliance

```bash
# Register user with GDPR consent tracking
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/registerUser \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "dateOfBirth": "1990-05-15",
    "phone": "+46701234567",
    "marketingConsent": true,
    "cookieConsent": true,
    "consentVersion": "2.1",
    "ipAddress": "192.168.1.100",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }'
```

### Create GDPR-Compliant Order

```bash
# Create order with GDPR compliance
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/createOrder \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_123",
    "items": [
      {
        "productId": "prod_organic_tshirt",
        "name": "Organic Cotton T-Shirt",
        "price": 29.99,
        "quantity": 2
      },
      {
        "productId": "prod_sustainable_jeans",
        "name": "Sustainable Jeans",
        "price": 89.99,
        "quantity": 1
      }
    ],
    "shippingAddress": {
      "street": "Kungsgatan 12",
      "city": "Stockholm",
      "postalCode": "11143",
      "country": "Sweden"
    },
    "billingAddress": {
      "street": "Kungsgatan 12",
      "city": "Stockholm",
      "postalCode": "11143",
      "country": "Sweden"
    },
    "paymentMethodId": "pm_1234567890abcdef",
    "totalAmount": 149.97,
    "currency": "EUR"
  }'
```

### GDPR Data Subject Rights

```bash
# Request user data access (GDPR Article 15)
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/handleDataSubjectRequest \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_123",
    "userEmail": "john.doe@example.com",
    "requestType": "access"
  }'
```

```bash
# Request data erasure (GDPR Article 17)
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/handleDataSubjectRequest \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_123",
    "userEmail": "john.doe@example.com",
    "requestType": "erasure"
  }'
```

```bash
# Download user data file (after access request)
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/downloadComplianceFile?file_id=FILE_ID_FROM_ACCESS_REQUEST" \
  -o "user_data_export.json"
```

### Consent Management

```bash
# Update marketing consent
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/updateConsent \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_123",
    "consentType": "marketing",
    "consentGiven": false,
    "consentVersion": "2.1",
    "ipAddress": "192.168.1.100",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }'
```

```bash
# Update cookie consent
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/updateConsent \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_123",
    "consentType": "cookies",
    "consentGiven": true,
    "consentVersion": "2.1",
    "ipAddress": "192.168.1.100",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }'
```

## 📁 File Management Operations

### Save Text Files to Firestore

```bash
# Save a simple text file
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/saveTextFile \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "project_notes.txt",
    "content": "# Project Notes\n\nThis is a sample project documentation file.\n\n## Features\n- User authentication\n- Product catalog\n- Shopping cart\n- Payment processing",
    "user_id": "developer_123",
    "tags": ["documentation", "project", "notes"],
    "is_public": false,
    "metadata": {
      "description": "Project documentation and notes",
      "category": "documentation",
      "version": "1.0"
    }
  }'
```

```bash
# Save configuration file
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/saveTextFile \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "app_config.json",
    "content": "{\n  \"apiEndpoint\": \"https://api.example.com\",\n  \"theme\": {\n    \"primaryColor\": \"#007bff\",\n    \"secondaryColor\": \"#6c757d\"\n  },\n  \"features\": {\n    \"darkMode\": true,\n    \"notifications\": true\n  }\n}",
    "user_id": "developer_123",
    "tags": ["config", "json", "settings"],
    "metadata": {
      "type": "configuration",
      "environment": "production"
    }
  }'
```

### Download Files from Firestore

```bash
# Download file by ID
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/downloadFile?file_id=FILE_ID_HERE" \
  -o "downloaded_file.txt"
```

```bash
# Get file metadata without downloading content
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/getFileInfo?file_id=FILE_ID_HERE"
```

### List and Search Files

```bash
# List user files
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/listUserFiles?user_id=developer_123&limit=10&page=0"
```

```bash
# List files with tag filter
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/listUserFiles?user_id=developer_123&tags=documentation,project"
```

```bash
# Search files by multiple criteria
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/searchFiles?user_id=developer_123&tags=config,json&content_type=text/plain&limit=20"
```

### Bulk File Operations

```bash
# Bulk save multiple files
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/bulkSaveFiles \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "developer_123",
    "files": [
      {
        "filename": "readme.md",
        "content": "# Project README\n\nThis is the main project documentation.",
        "tags": ["documentation", "readme"],
        "metadata": {"type": "documentation"}
      },
      {
        "filename": "changelog.txt",
        "content": "# Changelog\n\nv1.0.0 - Initial release",
        "tags": ["changelog", "version"],
        "metadata": {"type": "changelog"}
      },
      {
        "filename": "api_keys.txt",
        "content": "# API Keys\n\nDEV_API_KEY=dev_key_123\nPROD_API_KEY=prod_key_456",
        "tags": ["config", "api", "keys"],
        "metadata": {"type": "configuration", "sensitive": true}
      }
    ]
  }'
```

## 📊 Compliance and Audit Operations

### Query User Orders

```bash
# Get user orders with GDPR compliance
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/getUserOrders?userId=user_123&limit=10"
```

```bash
# Get orders by status
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/getUserOrders?userId=user_123&status=completed&limit=5"
```

### GDPR Audit Trail

```bash
# Get user audit trail
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/getGDPRAuditTrail?userId=user_123&limit=20"
```

```bash
# Get specific action audit trail
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/getGDPRAuditTrail?userId=user_123&action=consent_updated&limit=10"
```

### Generate Compliance Reports

```bash
# Generate monthly GDPR compliance report
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/generateGDPRComplianceReport \
  -H "Content-Type: application/json" \
  -d '{
    "reportType": "monthly",
    "startDate": "2024-01-01",
    "endDate": "2024-01-31"
  }'
```

```bash
# Download compliance report
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/downloadComplianceReport?report_id=REPORT_ID_HERE" \
  -o "gdpr_compliance_report.txt"
```

### Privacy-Aware Product Search

```bash
# Anonymous product search (privacy-first)
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/searchProducts \
  -H "Content-Type: application/json" \
  -d '{
    "query": "organic cotton",
    "category": "clothing",
    "priceRange": {"min": 20, "max": 100},
    "userId": null,
    "trackingConsent": false
  }'
```

```bash
# Authenticated search with tracking consent
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/searchProducts \
  -H "Content-Type: application/json" \
  -d '{
    "query": "sustainable fashion",
    "category": "clothing",
    "userId": "user_123",
    "trackingConsent": true
  }'
```

## 🔄 Batch Operations and Automation

### Automated Project Plan Generation

```bash
# Generate multiple project plans
for project in "Fashion Store" "Tech Blog" "Food Delivery"; do
  curl -X POST \
    https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan \
    -H "Content-Type: application/json" \
    -d "{
      \"project_name\": \"$project\",
      \"project_type\": \"webapp\",
      \"complexity\": \"medium\",
      \"tech_stack\": \"React, Node.js, MongoDB\"
    }" \
    -o "${project// /_}_plan.txt"
done
```

### File Management Automation

```bash
# Create project structure files
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/bulkSaveFiles \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "project_manager_456",
    "files": [
      {
        "filename": "project_charter.md",
        "content": "# Project Charter\n\n## Objectives\n- Define project scope\n- Establish timeline\n- Identify stakeholders",
        "tags": ["charter", "planning", "management"]
      },
      {
        "filename": "requirements.txt",
        "content": "# Requirements\n\n## Functional Requirements\n1. User authentication\n2. Product catalog\n3. Shopping cart",
        "tags": ["requirements", "specifications"]
      },
      {
        "filename": "architecture.md",
        "content": "# System Architecture\n\n## Components\n- Frontend: React\n- Backend: Node.js\n- Database: MongoDB",
        "tags": ["architecture", "technical", "design"]
      }
    ]
  }'
```

## 🛠️ Advanced Usage Examples

### Complete E-commerce Setup Workflow

```bash
#!/bin/bash
# Complete e-commerce project setup

# 1. Generate project plan
echo "Generating project plan..."
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Eco-Friendly Store",
    "project_type": "ecommerce",
    "complexity": "high",
    "tech_stack": "Next.js, Stripe, PostgreSQL, Redis",
    "deadline_weeks": 16
  }' \
  -o "eco_store_project_plan.txt"

# 2. Create project requirements in Firestore
echo "Storing project requirements..."
PROJECT_RESPONSE=$(curl -s -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Eco-Friendly Store",
    "project_type": "ecommerce",
    "complexity": "high",
    "tech_stack": "Next.js, Stripe, PostgreSQL, Redis",
    "deadline_weeks": 16,
    "user_id": "project_lead_789"
  }')

PROJECT_ID=$(echo $PROJECT_RESPONSE | jq -r '.id')
echo "Project stored with ID: $PROJECT_ID"

# 3. Save project documentation
echo "Creating project documentation..."
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/saveTextFile \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "project_overview.md",
    "content": "# Eco-Friendly Store Project\n\n## Overview\nBuilding a sustainable e-commerce platform with GDPR compliance.\n\n## Key Features\n- Sustainable product catalog\n- Carbon footprint tracking\n- GDPR-compliant user management\n- Eco-friendly shipping options",
    "user_id": "project_lead_789",
    "tags": ["project", "overview", "ecommerce", "sustainability"],
    "metadata": {
      "project_id": "'$PROJECT_ID'",
      "category": "documentation",
      "phase": "planning"
    }
  }'

echo "E-commerce project setup complete!"
```

### GDPR Compliance Audit Workflow

```bash
#!/bin/bash
# GDPR compliance audit workflow

USER_ID="user_123"
USER_EMAIL="john.doe@example.com"

# 1. Generate compliance report
echo "Generating GDPR compliance report..."
REPORT_RESPONSE=$(curl -s -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/generateGDPRComplianceReport \
  -H "Content-Type: application/json" \
  -d '{
    "reportType": "monthly",
    "startDate": "2024-01-01",
    "endDate": "2024-01-31"
  }')

REPORT_ID=$(echo $REPORT_RESPONSE | jq -r '.reportId')

# 2. Download compliance report
echo "Downloading compliance report..."
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/downloadComplianceReport?report_id=$REPORT_ID" \
  -o "gdpr_compliance_report_$(date +%Y%m%d).txt"

# 3. Get user audit trail
echo "Retrieving user audit trail..."
curl -X GET \
  "https://us-central1-mcptest-468919.cloudfunctions.net/getGDPRAuditTrail?userId=$USER_ID&limit=50" \
  -o "user_audit_trail_$(date +%Y%m%d).json"

# 4. Process data access request
echo "Processing data access request..."
ACCESS_RESPONSE=$(curl -s -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/handleDataSubjectRequest \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "userEmail": "'$USER_EMAIL'",
    "requestType": "access"
  }')

FILE_ID=$(echo $ACCESS_RESPONSE | jq -r '.fileId')

# 5. Download user data export
if [ "$FILE_ID" != "null" ]; then
  echo "Downloading user data export..."
  curl -X GET \
    "https://us-central1-mcptest-468919.cloudfunctions.net/downloadComplianceFile?file_id=$FILE_ID" \
    -o "user_data_export_$(date +%Y%m%d).json"
fi

echo "GDPR compliance audit complete!"
```

## 📝 Response Examples

### Successful File Download Response
```bash
# Command
curl -X POST \
  https://us-central1-mcptest-468919.cloudfunctions.net/downloadTextPlan \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "CouchBase Store",
    "project_type": "ecommerce",
    "complexity": "medium",
    "tech_stack": "React, Node.js, CouchBase"
  }' \
  -o "couchbase_store_plan.txt"

# Response Headers
Content-Type: text/plain
Content-Disposition: attachment; filename="CouchBase_Store_Project_Plan.txt"
Content-Length: 15420

# File Content (couchbase_store_plan.txt)
PROJECT DEVELOPMENT PLAN & GUIDELINES

Project Name: CouchBase Store
Project Type: ECOMMERCE
Complexity Level: MEDIUM
Generated Date: 14/08/2025
Estimated Timeline: 1-3 months
Budget Range: $15,000 - $50,000 USD
...
```

### File Save Response
```json
{
  "id": "abc123def456",
  "message": "File saved successfully",
  "filename": "project_notes.txt",
  "size": 1024,
  "download_url": "https://us-central1-mcptest-468919.cloudfunctions.net/downloadFile?file_id=abc123def456"
}
```

### GDPR Data Access Response
```json
{
  "requestId": "req_789xyz",
  "status": "completed",
  "message": "Data access request processed successfully",
  "downloadUrl": "https://us-central1-mcptest-468919.cloudfunctions.net/downloadComplianceFile?file_id=file_456abc",
  "fileId": "file_456abc"
}
```

This comprehensive curl command guide provides everything you need to interact with your Firestore-based file operations and GDPR-compliant e-commerce system. All commands are ready to use with your deployed Firebase Functions.
