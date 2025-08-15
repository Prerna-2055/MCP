# 🔥 Firebase Integration Guide for Prompt Context Server

## Overview
This guide shows how to deploy your Prompt Context Server to Firebase Cloud Functions and integrate it with your Lovable frontend using Firestore for data persistence.

## 🚀 Benefits of Firebase Integration

- **Serverless**: No server management required
- **Scalable**: Automatically scales with usage
- **Persistent Storage**: Save user projects and templates in Firestore
- **Authentication**: Built-in user authentication
- **Real-time**: Real-time database updates
- **Global CDN**: Fast worldwide access

## 📋 Prerequisites

1. **Firebase Account**: Create a free account at [firebase.google.com](https://firebase.google.com)
2. **Firebase CLI**: Install globally with `npm install -g firebase-tools`
3. **Node.js**: Version 18 or higher

## 🛠️ Setup Steps

### Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click "Create a project"
3. Enter project name (e.g., "prompt-context-server")
4. Enable Google Analytics (optional)
5. Create project

### Step 2: Enable Required Services

In your Firebase Console:

1. **Firestore Database**:
   - Go to "Firestore Database"
   - Click "Create database"
   - Choose "Start in test mode" (we'll secure it later)
   - Select a location

2. **Cloud Functions**:
   - Go to "Functions"
   - Click "Get started"
   - Upgrade to Blaze plan (pay-as-you-go, includes generous free tier)

3. **Authentication** (Optional but recommended):
   - Go to "Authentication"
   - Click "Get started"
   - Enable "Anonymous" and/or "Google" sign-in

### Step 3: Initialize Firebase Project Locally

```bash
# Navigate to the firebase-integration directory
cd firebase-integration

# Login to Firebase
firebase login

# Initialize Firebase project
firebase init

# Select:
# - Functions: Configure and deploy Cloud Functions
# - Firestore: Deploy rules and create indexes
# - Hosting: Configure and deploy Firebase Hosting sites

# Choose your existing project
# Select JavaScript for Functions
# Install dependencies with npm: Yes
```

### Step 4: Deploy Firebase Functions

```bash
# Navigate to functions directory
cd functions

# Install dependencies
npm install

# Deploy functions
firebase deploy --only functions
```

### Step 5: Deploy Firestore Rules

```bash
# Deploy security rules
firebase deploy --only firestore:rules
```

### Step 6: Get Your Function URLs

After deployment, you'll see URLs like:
```
https://us-central1-your-project-id.cloudfunctions.net/collectRequirements
https://us-central1-your-project-id.cloudfunctions.net/getBaseTemplates
https://us-central1-your-project-id.cloudfunctions.net/getAdvancedTemplate
https://us-central1-your-project-id.cloudfunctions.net/getUserProjects
```

## 🔧 Lovable Integration

### Step 1: Copy Firebase Components

Copy these files to your Lovable project:

1. **Copy `lovable-components/useFirebaseAPI.js`** to `src/hooks/useFirebaseAPI.js`
2. **Copy `lovable-components/ProjectRequirements.jsx`** to `src/components/ProjectRequirements.jsx`

### Step 2: Update Firebase Function URLs

In `src/hooks/useFirebaseAPI.js`, update the base URL:

```javascript
// Replace with your actual Firebase project URLs
const FIREBASE_FUNCTIONS_BASE = 'https://us-central1-your-project-id.cloudfunctions.net';
```

### Step 3: Use in Your Lovable App

```javascript
import { ProjectRequirements } from './components/ProjectRequirements';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Prompt Context Server
        </h1>
        <ProjectRequirements userId="user123" />
      </div>
    </div>
  );
}
```

## 🔐 Security Configuration

### Production Security Rules

Update `firestore.rules` for production:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /project_requirements/{document} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.user_id;
      allow create: if request.auth != null && request.auth.uid == request.resource.data.user_id;
    }
    
    match /template_requests/{document} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.user_id;
      allow create: if request.auth != null && request.auth.uid == request.resource.data.user_id;
    }
    
    match /advanced_templates/{document} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.user_id;
      allow create: if request.auth != null && request.auth.uid == request.resource.data.user_id;
    }
  }
}
```

## 🔄 Connecting to Your MCP Server

### Option 1: Replace Mock Functions

In `functions/index.js`, replace the `mockMCPTools` with actual calls to your MCP server:

```javascript
// Instead of mockMCPTools.collectRequirements(params)
// Make HTTP request to your local MCP server or integrate directly

const axios = require('axios');

const callMCPServer = async (endpoint, params) => {
  try {
    const response = await axios.post(`http://your-mcp-server:8000/${endpoint}`, params);
    return response.data;
  } catch (error) {
    console.error('MCP Server error:', error);
    throw error;
  }
};
```

### Option 2: Deploy MCP Server to Cloud

Deploy your MCP server to a cloud provider (Railway, Render, etc.) and call it from Firebase Functions.

## 📊 Data Structure

### Firestore Collections

**project_requirements**:
```json
{
  "id": "auto-generated",
  "project_name": "MyApp",
  "project_type": "webapp",
  "complexity": "medium",
  "tech_stack": "React + Node.js",
  "deadline_weeks": 6,
  "suggested_architecture": "SPA with component-based architecture",
  "phases": ["Phase 1", "Phase 2", ...],
  "risks": ["Risk 1", "Risk 2", ...],
  "user_id": "user123",
  "created_at": "timestamp"
}
```

**template_requests**:
```json
{
  "id": "auto-generated",
  "use_case": "webapp",
  "templates": ["Template 1", "Template 2", ...],
  "user_id": "user123",
  "created_at": "timestamp"
}
```

**advanced_templates**:
```json
{
  "id": "auto-generated",
  "base_template": "Original template",
  "style": "clean_code",
  "enhanced_template": "Enhanced template with guidance",
  "user_id": "user123",
  "created_at": "timestamp"
}
```

## 🧪 Testing

### Local Development

```bash
# Start Firebase emulators
firebase emulators:start

# Your functions will be available at:
# http://localhost:5001/your-project-id/us-central1/collectRequirements
```

### Test with curl

```bash
curl -X POST http://localhost:5001/your-project-id/us-central1/collectRequirements \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "TestApp",
    "project_type": "webapp",
    "complexity": "medium",
    "tech_stack": "React",
    "deadline_weeks": 4,
    "user_id": "test-user"
  }'
```

## 💰 Cost Considerations

Firebase offers generous free tiers:

- **Cloud Functions**: 2M invocations/month free
- **Firestore**: 50K reads, 20K writes/day free
- **Hosting**: 10GB storage, 360MB/day transfer free

For most applications, you'll stay within the free tier.

## 🚀 Deployment Commands

```bash
# Deploy everything
firebase deploy

# Deploy only functions
firebase deploy --only functions

# Deploy only Firestore rules
firebase deploy --only firestore:rules

# Deploy only hosting
firebase deploy --only hosting
```

## 🔍 Monitoring

- **Firebase Console**: View function logs, Firestore data, and usage metrics
- **Cloud Logging**: Detailed function execution logs
- **Performance Monitoring**: Track function performance

## 🎉 Benefits Over Local Server

1. **No Server Management**: Firebase handles scaling, security, and maintenance
2. **Global Distribution**: Your API is available worldwide with low latency
3. **Automatic Scaling**: Handles traffic spikes automatically
4. **Data Persistence**: User projects and templates are saved permanently
5. **User Management**: Built-in authentication and user management
6. **Real-time Updates**: Firestore provides real-time data synchronization

Your Prompt Context Server is now production-ready with Firebase! 🔥
