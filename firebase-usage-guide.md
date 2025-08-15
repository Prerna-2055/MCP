# 🔥 Using Advanced Process Automation Tool via Firebase

## 🚀 Firebase Cloud Function Usage

### **Function URL (after deployment):**
```
https://us-central1-mcptest-468919.cloudfunctions.net/analyzeProcessAutomation
```

### **HTTP Request Example:**
```bash
curl -X POST https://us-central1-mcptest-468919.cloudfunctions.net/analyzeProcessAutomation \
  -H "Content-Type: application/json" \
  -d '{
    "process_name": "New Employee Onboarding",
    "primary_goal": "save_time",
    "trigger_type": "form_submission",
    "trigger_details": "HR submits new hire form with employee details",
    "success_outcome": "Employee has access to all systems and receives welcome package",
    "current_steps": "Manual form processing, IT setup, manager assignment",
    "stakeholders": "HR, IT, Direct Manager, Facilities",
    "frequency": "5-10 new hires per month",
    "pain_points": "Manual coordination, delayed system access",
    "user_id": "user123"
  }'
```

## 📱 React Component for Firebase

### **Updated Hook with Advanced Tool:**
```javascript
// Add to your useFirebaseAPI.js hook
const analyzeProcessAutomation = async (params, userId = 'anonymous') => {
  setLoading(true);
  setError(null);
  
  try {
    const response = await analyzeProcessAutomationFunction({
      process_name: params.processName,
      primary_goal: params.primaryGoal,
      trigger_type: params.triggerType,
      trigger_details: params.triggerDetails,
      success_outcome: params.successOutcome,
      current_steps: params.currentSteps || 'not specified',
      stakeholders: params.stakeholders || 'not specified',
      frequency: params.frequency || 'not specified',
      pain_points: params.painPoints || 'not specified',
      user_id: userId
    });

    return response.data;
  } catch (err) {
    setError(err.message || 'An error occurred');
    return null;
  } finally {
    setLoading(false);
  }
};

// Add to your hook's return statement
return {
  collectRequirements,
  getBaseTemplates,
  getAdvancedTemplate,
  analyzeProcessAutomation, // New advanced tool
  getUserProjects,
  loading,
  error,
};
```

### **React Component for Process Automation:**
```jsx
import { useState } from 'react';
import { useFirebaseAPI } from '../hooks/useFirebaseAPI';

export const ProcessAutomationAnalyzer = ({ userId = 'anonymous' }) => {
  const { analyzeProcessAutomation, loading, error } = useFirebaseAPI();
  const [formData, setFormData] = useState({
    processName: '',
    primaryGoal: 'save_time',
    triggerType: 'form_submission',
    triggerDetails: '',
    successOutcome: '',
    currentSteps: '',
    stakeholders: '',
    frequency: '',
    painPoints: ''
  });
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await analyzeProcessAutomation(formData, userId);
    setResult(response);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        Advanced Process Automation Analyzer
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Process Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Process Name *
          </label>
          <input
            type="text"
            name="processName"
            value={formData.processName}
            onChange={handleInputChange}
            placeholder="e.g., New Employee Onboarding, Customer Invoice Approval"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            A short, descriptive name for the process you want to automate
          </p>
        </div>

        {/* Primary Goal */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Primary Goal *
          </label>
          <select
            name="primaryGoal"
            value={formData.primaryGoal}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="save_time">Save Time / Increase Speed</option>
            <option value="reduce_errors">Reduce Manual Errors</option>
            <option value="improve_compliance">Improve Compliance / Audit Trail</option>
            <option value="enhance_visibility">Enhance Visibility / Reporting</option>
            <option value="standardize_process">Standardize the Process</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">
            The single most important goal of automating this process
          </p>
        </div>

        {/* Trigger Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Trigger Type *
          </label>
          <select
            name="triggerType"
            value={formData.triggerType}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="email">Email Arrives (e.g., invoices@company.com)</option>
            <option value="form_submission">Form Submission (e.g., Google Form, Typeform)</option>
            <option value="system_record">System Record Created (e.g., new Lead in Salesforce)</option>
            <option value="schedule">Recurring Schedule (e.g., every Monday at 9 AM)</option>
            <option value="manual">Manual Trigger (user clicks button)</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">
            What event kicks off this process?
          </p>
        </div>

        {/* Trigger Details */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Trigger Details *
          </label>
          <textarea
            name="triggerDetails"
            value={formData.triggerDetails}
            onChange={handleInputChange}
            placeholder="e.g., Invoice received at invoices@company.com with PDF attachment"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            Specific details about how the process starts
          </p>
        </div>

        {/* Success Outcome */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Success Outcome *
          </label>
          <textarea
            name="successOutcome"
            value={formData.successOutcome}
            onChange={handleInputChange}
            placeholder="e.g., Employee has access to all systems and receives welcome package"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            How do you know the process has finished successfully?
          </p>
        </div>

        {/* Optional Fields */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Current Steps
            </label>
            <textarea
              name="currentSteps"
              value={formData.currentSteps}
              onChange={handleInputChange}
              placeholder="e.g., Manual form processing, IT setup, manager assignment"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Stakeholders
            </label>
            <textarea
              name="stakeholders"
              value={formData.stakeholders}
              onChange={handleInputChange}
              placeholder="e.g., HR, IT, Direct Manager, Facilities"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Frequency
            </label>
            <input
              type="text"
              name="frequency"
              value={formData.frequency}
              onChange={handleInputChange}
              placeholder="e.g., 5-10 times per month"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Pain Points
            </label>
            <input
              type="text"
              name="painPoints"
              value={formData.painPoints}
              onChange={handleInputChange}
              placeholder="e.g., Manual coordination, delays, errors"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-purple-600 text-white py-3 px-6 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50 text-lg font-medium"
        >
          {loading ? 'Analyzing Process...' : 'Generate Advanced Analysis'}
        </button>
      </form>

      {error && (
        <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          Error: {error}
        </div>
      )}

      {result && (
        <div className="mt-8 space-y-6">
          <h3 className="text-xl font-bold text-gray-800">Process Automation Analysis</h3>
          
          {/* Process Overview */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">Process Overview</h4>
            <p><strong>Name:</strong> {result.process_overview.name}</p>
            <p><strong>Focus:</strong> {result.process_overview.focus_area}</p>
            <p><strong>Trigger:</strong> {result.process_overview.trigger_details}</p>
          </div>

          {/* Automation Strategy */}
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">Automation Strategy</h4>
            <p><strong>Approach:</strong> {result.automation_strategy.implementation_approach}</p>
            <div className="mt-2">
              <strong>Key Recommendations:</strong>
              <ul className="list-disc list-inside ml-4 mt-1">
                {result.automation_strategy.key_recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Implementation Phases */}
          <div className="bg-yellow-50 p-4 rounded-lg">
            <h4 className="font-semibold text-yellow-800 mb-2">5-Phase Implementation</h4>
            {Object.entries(result.detailed_implementation).map(([phase, steps]) => (
              <div key={phase} className="mb-3">
                <strong className="capitalize">{phase.replace('_', ' ')}:</strong>
                <ul className="list-disc list-inside ml-4 mt-1">
                  {steps.map((step, index) => (
                    <li key={index} className="text-sm">{step}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Risk Assessment */}
          <div className="bg-red-50 p-4 rounded-lg">
            <h4 className="font-semibold text-red-800 mb-2">Risk Assessment</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <strong>Technical Risks:</strong>
                <ul className="list-disc list-inside ml-4 mt-1 text-sm">
                  {result.risk_assessment.technical_risks.map((risk, index) => (
                    <li key={index}>{risk}</li>
                  ))}
                </ul>
              </div>
              <div>
                <strong>Business Risks:</strong>
                <ul className="list-disc list-inside ml-4 mt-1 text-sm">
                  {result.risk_assessment.business_risks.map((risk, index) => (
                    <li key={index}>{risk}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Success Framework */}
          <div className="bg-purple-50 p-4 rounded-lg">
            <h4 className="font-semibold text-purple-800 mb-2">Success Framework</h4>
            <p><strong>KPIs:</strong> {result.success_framework.kpis.join(', ')}</p>
            <p><strong>Monitoring:</strong> {result.success_framework.monitoring_approach}</p>
            <p><strong>Review Schedule:</strong> {result.success_framework.review_schedule}</p>
          </div>

          {/* Next Steps */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-800 mb-2">Next Steps</h4>
            <ol className="list-decimal list-inside space-y-1">
              {result.next_steps.map((step, index) => (
                <li key={index} className="text-sm">{step}</li>
              ))}
            </ol>
          </div>

          {result.id && (
            <p className="text-sm text-gray-500 mt-4">
              <strong>Saved to Firebase:</strong> {result.id}
            </p>
          )}
        </div>
      )}
    </div>
  );
};
```

## 🎯 **Example Use Cases:**

### **1. Employee Onboarding**
```json
{
  "process_name": "New Employee Onboarding",
  "primary_goal": "save_time",
  "trigger_type": "form_submission",
  "trigger_details": "HR submits new hire form with employee details",
  "success_outcome": "Employee has access to all systems and receives welcome package"
}
```

### **2. Invoice Processing**
```json
{
  "process_name": "Customer Invoice Approval",
  "primary_goal": "improve_compliance",
  "trigger_type": "email",
  "trigger_details": "Invoice received at invoices@company.com with PDF attachment",
  "success_outcome": "Invoice is approved/rejected with audit trail and payment processed"
}
```

### **3. Sales Lead Qualification**
```json
{
  "process_name": "Sales Lead Qualification",
  "primary_goal": "enhance_visibility",
  "trigger_type": "system_record",
  "trigger_details": "New lead created in Salesforce with contact information",
  "success_outcome": "Lead is qualified/disqualified with score and next action assigned"
}
```

## 📊 **What You Get Back:**

### **Comprehensive Analysis Including:**
- **Process Overview**: Goal analysis and trigger details
- **Automation Strategy**: 4-5 specific recommendations based on your goal
- **5-Phase Implementation Plan**: Discovery → Design → Development → Testing → Deployment
- **Risk Assessment**: Technical and business risks with mitigation strategies
- **Success Framework**: KPIs, monitoring approach, review schedule
- **Next Steps**: Actionable items to get started

### **Goal-Specific Recommendations:**
- **Save Time**: Parallel processing, batch operations, caching
- **Reduce Errors**: Input validation, data quality checks, error workflows
- **Improve Compliance**: Audit trails, approval workflows, compliance checkpoints
- **Enhance Visibility**: Real-time dashboards, status notifications, progress tracking
- **Standardize Process**: Process templates, standard workflows, quality gates

### **Trigger-Specific Implementation:**
- **Email**: Email monitoring, parsing, attachment handling
- **Form Submission**: Webhook integration, data validation, field mapping
- **System Record**: Database triggers, API webhooks, event streaming
- **Schedule**: Cron jobs, task schedulers, retry mechanisms
- **Manual**: User interfaces, permissions, progress feedback

## 🚀 **Deploy and Use:**

1. **Deploy Firebase Functions**: `firebase deploy --only functions`
2. **Get Function URL**: Copy from deployment output
3. **Update your frontend**: Add the new component
4. **Start analyzing processes**: Get detailed automation roadmaps!

Your advanced process automation analyzer is ready to provide enterprise-level analysis! 🔥
