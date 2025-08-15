# 🔥 Firebase SDK Integration Guide for Lovable

## Overview
This guide shows how to integrate your Prompt Context Server with Firebase using the Firebase SDK v9+ with `httpsCallable` functions in your Lovable project.

## 📦 Step 1: Install Firebase SDK

In your Lovable project, install the Firebase SDK:

```bash
npm install firebase
```

## 🔧 Step 2: Firebase Configuration

### Copy Firebase Config File

Copy `firebase-integration/lovable-components/firebaseConfig.ts` to your Lovable project at `src/config/firebaseConfig.ts`:

```typescript
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getFunctions } from 'firebase/functions';
import { getAuth } from 'firebase/auth';

// Replace with your Firebase project configuration
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-app-id"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const db = getFirestore(app);
export const functions = getFunctions(app);
export const auth = getAuth(app);

export default app;
```

### Get Your Firebase Config

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project
3. Go to Project Settings (gear icon)
4. Scroll down to "Your apps"
5. Click "Config" to see your configuration object
6. Replace the values in `firebaseConfig.ts`

## 🪝 Step 3: Copy Firebase Hook

Copy `firebase-integration/lovable-components/useFirebaseAPI.ts` to your Lovable project at `src/hooks/useFirebaseAPI.ts`:

```typescript
import { useState } from 'react';
import { httpsCallable } from 'firebase/functions';
import { functions } from '../config/firebaseConfig';

// ... (full hook code as provided)
```

## 📱 Step 4: Copy React Component

Copy `firebase-integration/lovable-components/ProjectRequirements.tsx` to your Lovable project at `src/components/ProjectRequirements.tsx`:

```typescript
import { useState } from 'react';
import { useFirebaseAPI } from '../hooks/useFirebaseAPI';

// ... (full component code as provided)
```

## 🚀 Step 5: Deploy Firebase Functions

### Deploy Your Cloud Functions

```bash
cd firebase-integration
firebase login
firebase init
firebase deploy --only functions
```

### Update Function Names (if needed)

Make sure your Cloud Function names match what's in the hook:

- `collectRequirements`
- `getBaseTemplates` 
- `getAdvancedTemplate`
- `getUserProjects`

## 🎯 Step 6: Use in Your Lovable App

### Import and Use the Component

```typescript
// In your App.tsx or any page component
import { ProjectRequirements } from './components/ProjectRequirements';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          AI Project Requirements Generator
        </h1>
        <ProjectRequirements userId="user123" />
      </div>
    </div>
  );
}

export default App;
```

### With Authentication (Optional)

```typescript
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from './config/firebaseConfig';
import { ProjectRequirements } from './components/ProjectRequirements';

function App() {
  const [user, loading, error] = useAuthState(auth);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          AI Project Requirements Generator
        </h1>
        <ProjectRequirements userId={user?.uid || 'anonymous'} />
      </div>
    </div>
  );
}
```

## 🔐 Step 7: Security Rules

Deploy your Firestore security rules:

```bash
firebase deploy --only firestore:rules
```

## 🧪 Step 8: Testing

### Test Firebase Functions Locally

```bash
# Start Firebase emulators
firebase emulators:start

# Test with your Lovable app pointing to local functions
```

### Test in Production

1. Deploy functions: `firebase deploy --only functions`
2. Update your Lovable app to use production Firebase config
3. Test the integration

## 📊 Key Benefits of Firebase SDK Approach

✅ **Type Safety**: Full TypeScript support with proper types  
✅ **Better Error Handling**: Firebase SDK provides detailed error information  
✅ **Automatic Retries**: Built-in retry logic for failed requests  
