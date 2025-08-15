# 🧪 Testing Your Deployed Firebase Functions

## 🔥 Your Firebase Project: mcptest-468919

### **Firebase Console**: https://console.firebase.google.com/project/mcptest-468919/overview

## 🚀 **Step 1: Find Your Function URLs**

1. **Go to Firebase Console**: https://console.firebase.google.com/project/mcptest-468919/functions
2. **Look for your deployed functions**:
   - `analyzeProcessAutomation`
   - `collectRequirements`
   - `getBaseTemplates`
   - `getAdvancedTemplate`
   - `getUserProjects`

3. **Copy the function URLs** - they should look like:
   ```
   https://us-central1-mcptest-468919.cloudfunctions.net/analyzeProcessAutomation
   https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements
   ```

## 🧪 **Step 2: Test Functions with curl**

### **Test 1: Advanced Process Automation (New Tool)**
```bash
curl -X POST https://us-central1-mcptest-468919.cloudfunctions.net/analyzeProcessAutomation \
  -H "Content-Type: application/json" \
  -d '{
    "process_name": "Customer Invoice Approval",
    "primary_goal": "improve_compliance",
    "trigger_type": "email",
    "trigger_details": "Invoice received at invoices@company.com with PDF attachment",
    "success_outcome": "Invoice is approved/rejected with complete audit trail and payment processed",
    "current_steps": "Manual email review, manager approval, accounting entry",
    "stakeholders": "Accounting, Finance Manager, Accounts Payable",
    "frequency": "50-100 invoices per week",
    "pain_points": "Approval delays, missing audit trails, manual data entry errors",
    "user_id": "test-user"
  }'
```

### **Test 2: Collect Requirements**
```bash
curl -X POST https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "E-commerce Platform",
    "project_type": "webapp",
    "complexity": "high",
    "tech_stack": "React + Node.js + PostgreSQL",
    "deadline_weeks": 12,
    "user_id": "test-user"
  }'
```

### **Test 3: Get Base Templates**
```bash
curl -X POST https://us-central1-mcptest-468919.cloudfunctions.net/getBaseTemplates \
  -H "Content-Type: application/json" \
  -d '{
    "use_case": "api",
    "user_id": "test-user"
  }'
```

### **Test 4: Get Advanced Template**
```bash
curl -X POST https://us-central1-mcptest-468919.cloudfunctions.net/getAdvancedTemplate \
  -H "Content-Type: application/json" \
  -d '{
    "base_template": "Design REST endpoints for user management system",
    "style": "security_first",
    "user_id": "test-user"
  }'
```

## 📊 **Step 3: Test Through Firebase Console**

### **Using Firebase Console Test Interface:**

1. **Go to Functions**: https://console.firebase.google.com/project/mcptest-468919/functions
2. **Click on any function** (e.g., `analyzeProcessAutomation`)
3. **Click "Test function"** tab
4. **Enter test data**:
   ```json
   {
     "data": {
       "process_name": "Sales Lead Qualification",
       "primary_goal": "enhance_visibility",
       "trigger_type": "system_record",
       "trigger_details": "New lead created in Salesforce with contact information",
       "success_outcome": "Lead is qualified/disqualified with score and next action assigned",
       "user_id": "test-user"
     }
   }
   ```
5. **Click "Test the function"**
6. **View results** in the console

## 📱 **Step 4: Test with Postman/Insomnia**

### **Import this collection:**
```json
{
  "name": "Prompt Context Server - Firebase",
  "requests": [
    {
      "name": "Analyze Process Automation",
      "method": "POST",
      "url": "https://us-central1-mcptest-468919.cloudfunctions.net/analyzeProcessAutomation",
      "headers": {
        "Content-Type": "application/json"
      },
      "body": {
        "process_name": "New Employee Onboarding",
        "primary_goal": "save_time",
        "trigger_type": "form_submission",
        "trigger_details": "HR submits new hire form",
        "success_outcome": "Employee has system access",
        "user_id": "test-user"
      }
    }
  ]
}
```

## 🔍 **Step 5: Monitor Function Execution**

### **View Logs:**
1. **Go to Functions**: https://console.firebase.google.com/project/mcptest-468919/functions
2. **Click on a function**
3. **Click "Logs" tab**
4. **See real-time execution logs**

### **Monitor Performance:**
1. **Go to Functions dashboard**
2. **View metrics**: Invocations, execution time, errors
3. **Check usage**: Stay within free tier limits

## 📈 **Step 6: Check Firestore Data**

### **View Stored Data:**
1. **Go to Firestore**: https://console.firebase.google.com/project/mcptest-468919/firestore
2. **Check collections**:
   - `project_requirements` - Stored project analyses
   - `template_requests` - Template generation history
   - `advanced_templates` - Enhanced templates
   - `process_automation_analyses` - Advanced automation analyses

## 🎯 **Expected Results:**

### **Advanced Process Automation Response:**
```json
{
  "id": "firebase-document-id",
  "process_overview": {
    "name": "Customer Invoice Approval",
    "primary_goal": "improve_compliance",
    "focus_area": "Audit trails and regulatory adherence"
  },
  "automation_strategy": {
    "key_recommendations": [
      "Log all process steps with timestamps",
      "Implement approval workflows",
      "Create compliance checkpoints",
      "Generate audit reports automatically"
    ],
    "success_metrics": [
      "Audit trail completeness",
      "Compliance score", 
      "Documentation coverage"
    ]
  },
  "detailed_implementation": {
    "phase_1_discovery": [...],
    "phase_2_design": [...],
    "phase_3_development": [...],
    "phase_4_testing": [...],
    "phase_5_deployment": [...]
  },
  "risk_assessment": {
    "technical_risks": [...],
    "business_risks": [...],
    "mitigation_strategies": [...]
  },
  "success_framework": {
    "kpis": [...],
    "monitoring_approach": "Real-time dashboards with automated alerts"
  }
}
```

## 🚀 **Quick Test Commands:**

```bash
# Test the advanced tool
curl -X POST https://us-central1-mcptest-468919.cloudfunctions.net/analyzeProcessAutomation \
  -H "Content-Type: application/json" \
  -d '{"process_name":"Test Process","primary_goal":"save_time","trigger_type":"manual","trigger_details":"User clicks button","success_outcome":"Task completed","user_id":"test"}'

# Test requirements collection
curl -X POST https://us-central1-mcptest-468919.cloudfunctions.net/collectRequirements \
  -H "Content-Type: application/json" \
  -d '{"project_name":"Test App","project_type":"webapp","complexity":"medium","user_id":"test"}'
```

Your Firebase functions are now globally accessible and ready for enterprise-level process automation analysis! 🔥
