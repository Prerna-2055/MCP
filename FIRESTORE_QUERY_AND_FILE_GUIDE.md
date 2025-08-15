# 🔥 Complete Guide: Firestore Queries and File Operations

## Overview
This guide shows you how to create queries, save files directly to Firestore, and access them efficiently. Based on your existing Firebase setup, this covers both Cloud Functions and client-side operations.

## 📋 Table of Contents
1. [Firestore Data Structure](#firestore-data-structure)
2. [Creating Queries](#creating-queries)
3. [Saving Files to Firestore](#saving-files-to-firestore)
4. [Accessing Files from Firestore](#accessing-files-from-firestore)
5. [Advanced Query Patterns](#advanced-query-patterns)
6. [Security Rules](#security-rules)
7. [Practical Examples](#practical-examples)

## 🗂️ Firestore Data Structure

### Current Collections in Your Setup
```javascript
// Collections already implemented in your Firebase Functions
project_requirements/        // Project data and plans
template_requests/          // Template requests
advanced_templates/         // Enhanced templates
process_automation_analyses/ // Process automation data

// Recommended additional collections for file operations
files/                      // File metadata and content
user_files/                 // User-specific files
shared_files/              // Publicly accessible files
file_versions/             // File version history
```

### Document Structure Examples
```javascript
// project_requirements document
{
  id: "auto-generated",
  project_name: "MyApp",
  project_type: "webapp",
  complexity: "medium",
  tech_stack: "React + Node.js",
  text_plan: "Full project plan content...",
  plan_filename: "MyApp_Project_Plan.txt",
  user_id: "user123",
  created_at: timestamp,
  updated_at: timestamp
}

// files document (for storing file content)
{
  id: "auto-generated",
  filename: "project_plan.txt",
  content: "File content as string...",
  content_type: "text/plain",
  size: 1024,
  user_id: "user123",
  is_public: false,
  tags: ["project", "plan"],
  created_at: timestamp,
  updated_at: timestamp
}
```

## 🔍 Creating Queries

### 1. Basic Queries in Cloud Functions

```javascript
const admin = require('firebase-admin');
const db = admin.firestore();

// Get all documents from a collection
const getAllProjects = async () => {
  const snapshot = await db.collection('project_requirements').get();
  const projects = [];
  snapshot.forEach(doc => {
    projects.push({ id: doc.id, ...doc.data() });
  });
  return projects;
};

// Query with filters
const getProjectsByType = async (projectType) => {
  const snapshot = await db.collection('project_requirements')
    .where('project_type', '==', projectType)
    .orderBy('created_at', 'desc')
    .limit(10)
    .get();
  
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};

// Query with multiple conditions
const getComplexProjects = async (userId, complexity) => {
  const snapshot = await db.collection('project_requirements')
    .where('user_id', '==', userId)
    .where('complexity', '==', complexity)
    .where('created_at', '>', new Date('2024-01-01'))
    .orderBy('created_at', 'desc')
    .get();
  
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};
```

### 2. Client-Side Queries (JavaScript/React)

```javascript
import { initializeApp } from 'firebase/app';
import { 
  getFirestore, 
  collection, 
  query, 
  where, 
  orderBy, 
  limit, 
  getDocs,
  doc,
  getDoc,
  addDoc,
  updateDoc,
  deleteDoc
} from 'firebase/firestore';

const firebaseConfig = {
  // Your config
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Query files by user
const getUserFiles = async (userId) => {
  const q = query(
    collection(db, 'files'),
    where('user_id', '==', userId),
    orderBy('created_at', 'desc'),
    limit(20)
  );
  
  const querySnapshot = await getDocs(q);
  return querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};

// Search files by tags
const searchFilesByTags = async (tags) => {
  const q = query(
    collection(db, 'files'),
    where('tags', 'array-contains-any', tags),
    orderBy('created_at', 'desc')
  );
  
  const querySnapshot = await getDocs(q);
  return querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};
```

## 💾 Saving Files to Firestore

### 1. Save Text Files Directly in Documents

```javascript
// Cloud Function to save text file
exports.saveTextFile = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { filename, content, user_id, tags = [], is_public = false } = req.body;
      
      if (!filename || !content) {
        return res.status(400).json({ error: 'Missing filename or content' });
      }

      // Save file to Firestore
      const fileDoc = {
        filename,
        content,
        content_type: 'text/plain',
        size: Buffer.byteLength(content, 'utf8'),
        user_id: user_id || 'anonymous',
        tags,
        is_public,
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      };

      const docRef = await db.collection('files').add(fileDoc);

      res.json({
        id: docRef.id,
        message: 'File saved successfully',
        filename,
        size: fileDoc.size
      });

    } catch (error) {
      console.error('Error saving file:', error);
      res.status(500).json({ error: 'Failed to save file' });
    }
  });
});

// Enhanced version with automatic project plan generation
exports.saveProjectPlan = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { project_name, project_type, complexity, tech_stack, deadline_weeks, user_id } = req.body;
      
      // Generate project plan using existing logic
      const projectData = mockMCPTools.collectRequirements({
        project_name,
        project_type,
        complexity,
        tech_stack: tech_stack || 'not specified',
        deadline_weeks: deadline_weeks || 4
      });

      // Save to project_requirements collection
      const projectDoc = await db.collection('project_requirements').add({
        ...projectData,
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        user_id: user_id || 'anonymous'
      });

      // Also save as a downloadable file
      const filename = `${project_name.replace(/[^a-zA-Z0-9]/g, '_')}_Project_Plan.txt`;
      const fileDoc = await db.collection('files').add({
        filename,
        content: projectData.text_plan,
        content_type: 'text/plain',
        size: Buffer.byteLength(projectData.text_plan, 'utf8'),
        user_id: user_id || 'anonymous',
        tags: ['project_plan', project_type, complexity],
        is_public: false,
        project_id: projectDoc.id,
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      });

      res.json({
        project_id: projectDoc.id,
        file_id: fileDoc.id,
        filename,
        download_url: `${req.protocol}://${req.get('host')}/downloadFile?file_id=${fileDoc.id}`,
        ...projectData
      });

    } catch (error) {
      console.error('Error saving project plan:', error);
      res.status(500).json({ error: 'Failed to save project plan' });
    }
  });
});
```

### 2. Client-Side File Saving

```javascript
// React hook for saving files
import { useState } from 'react';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';

export const useFileSaver = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const saveFile = async (fileData) => {
    setLoading(true);
    setError(null);
    
    try {
      const docRef = await addDoc(collection(db, 'files'), {
        ...fileData,
        created_at: serverTimestamp(),
        updated_at: serverTimestamp()
      });
      
      setLoading(false);
      return { id: docRef.id, success: true };
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err;
    }
  };

  const saveTextFile = async (filename, content, userId, tags = []) => {
    return await saveFile({
      filename,
      content,
      content_type: 'text/plain',
      size: new Blob([content]).size,
      user_id: userId,
      tags,
      is_public: false
    });
  };

  return { saveFile, saveTextFile, loading, error };
};

// Usage in React component
const FileUploader = ({ userId }) => {
  const { saveTextFile, loading, error } = useFileSaver();
  const [content, setContent] = useState('');
  const [filename, setFilename] = useState('');

  const handleSave = async () => {
    try {
      const result = await saveTextFile(filename, content, userId, ['user_upload']);
      console.log('File saved:', result);
    } catch (err) {
      console.error('Save failed:', err);
    }
  };

  return (
    <div>
      <input 
        value={filename} 
        onChange={(e) => setFilename(e.target.value)}
        placeholder="Filename"
      />
      <textarea 
        value={content} 
        onChange={(e) => setContent(e.target.value)}
        placeholder="File content"
      />
      <button onClick={handleSave} disabled={loading}>
        {loading ? 'Saving...' : 'Save File'}
      </button>
      {error && <p>Error: {error}</p>}
    </div>
  );
};
```

## 📥 Accessing Files from Firestore

### 1. Download Files via Cloud Functions

```javascript
// Cloud Function to download files
exports.downloadFile = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { file_id } = req.query;
      
      if (!file_id) {
        return res.status(400).json({ error: 'Missing file_id parameter' });
      }

      // Get file from Firestore
      const fileDoc = await db.collection('files').doc(file_id).get();
      
      if (!fileDoc.exists) {
        return res.status(404).json({ error: 'File not found' });
      }

      const fileData = fileDoc.data();
      
      // Set headers for file download
      res.setHeader('Content-Type', fileData.content_type || 'text/plain');
      res.setHeader('Content-Disposition', `attachment; filename="${fileData.filename}"`);
      res.setHeader('Content-Length', Buffer.byteLength(fileData.content, 'utf8'));

      // Return file content
      res.send(fileData.content);

    } catch (error) {
      console.error('Error downloading file:', error);
      res.status(500).json({ error: 'Failed to download file' });
    }
  });
});

// Get file metadata without content
exports.getFileInfo = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { file_id } = req.query;
      
      const fileDoc = await db.collection('files').doc(file_id).get();
      
      if (!fileDoc.exists) {
        return res.status(404).json({ error: 'File not found' });
      }

      const fileData = fileDoc.data();
      
      // Return metadata without content
      const { content, ...metadata } = fileData;
      
      res.json({
        id: fileDoc.id,
        ...metadata,
        download_url: `${req.protocol}://${req.get('host')}/downloadFile?file_id=${file_id}`
      });

    } catch (error) {
      console.error('Error getting file info:', error);
      res.status(500).json({ error: 'Failed to get file info' });
    }
  });
});
```

### 2. Client-Side File Access

```javascript
// React hook for file operations
export const useFileManager = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadUserFiles = async (userId) => {
    setLoading(true);
    try {
      const q = query(
        collection(db, 'files'),
        where('user_id', '==', userId),
        orderBy('created_at', 'desc')
      );
      
      const querySnapshot = await getDocs(q);
      const fileList = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      
      setFiles(fileList);
    } catch (error) {
      console.error('Error loading files:', error);
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = async (fileId, filename) => {
    try {
      const fileDoc = await getDoc(doc(db, 'files', fileId));
      
      if (!fileDoc.exists()) {
        throw new Error('File not found');
      }

      const fileData = fileDoc.data();
      
      // Create download link
      const blob = new Blob([fileData.content], { type: fileData.content_type });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename || fileData.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Error downloading file:', error);
      throw error;
    }
  };

  return { files, loadUserFiles, downloadFile, loading };
};

// File browser component
const FileBrowser = ({ userId }) => {
  const { files, loadUserFiles, downloadFile, loading } = useFileManager();

  useEffect(() => {
    if (userId) {
      loadUserFiles(userId);
    }
  }, [userId]);

  return (
    <div>
      <h3>Your Files</h3>
      {loading ? (
        <p>Loading files...</p>
      ) : (
        <div>
          {files.map(file => (
            <div key={file.id} className="file-item">
              <span>{file.filename}</span>
              <span>{(file.size / 1024).toFixed(2)} KB</span>
              <button onClick={() => downloadFile(file.id, file.filename)}>
                Download
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

## 🔍 Advanced Query Patterns

### 1. Compound Queries

```javascript
// Multiple conditions with array operations
const searchFiles = async (userId, tags, contentType) => {
  let q = collection(db, 'files');
  
  // Build query dynamically
  const constraints = [where('user_id', '==', userId)];
  
  if (tags && tags.length > 0) {
    constraints.push(where('tags', 'array-contains-any', tags));
  }
  
  if (contentType) {
    constraints.push(where('content_type', '==', contentType));
  }
  
  constraints.push(orderBy('created_at', 'desc'));
  
  const finalQuery = query(q, ...constraints);
  const snapshot = await getDocs(finalQuery);
  
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};
```

### 2. Pagination

```javascript
// Paginated file listing
const getFilesPaginated = async (userId, lastDoc = null, pageSize = 10) => {
  let q = query(
    collection(db, 'files'),
    where('user_id', '==', userId),
    orderBy('created_at', 'desc'),
    limit(pageSize)
  );
  
  if (lastDoc) {
    q = query(q, startAfter(lastDoc));
  }
  
  const snapshot = await getDocs(q);
  const files = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  const lastVisible = snapshot.docs[snapshot.docs.length - 1];
  
  return { files, lastVisible, hasMore: files.length === pageSize };
};
```

### 3. Real-time Listeners

```javascript
// Real-time file updates
const useRealtimeFiles = (userId) => {
  const [files, setFiles] = useState([]);
  
  useEffect(() => {
    if (!userId) return;
    
    const q = query(
      collection(db, 'files'),
      where('user_id', '==', userId),
      orderBy('created_at', 'desc')
    );
    
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const fileList = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      setFiles(fileList);
    });
    
    return unsubscribe;
  }, [userId]);
  
  return files;
};
```

## 🔐 Security Rules

### Production-Ready Firestore Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Files collection - user can only access their own files
    match /files/{fileId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == resource.data.user_id;
      allow create: if request.auth != null && 
        request.auth.uid == request.resource.data.user_id;
    }
    
    // Public files - anyone can read, only owner can write
    match /files/{fileId} {
      allow read: if resource.data.is_public == true;
    }
    
    // Project requirements - user-specific access
    match /project_requirements/{docId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == resource.data.user_id;
      allow create: if request.auth != null && 
        request.auth.uid == request.resource.data.user_id;
    }
    
    // Shared files collection - different access patterns
    match /shared_files/{docId} {
      allow read: if true; // Public read
      allow write: if request.auth != null;
    }
  }
}
```

## 🛠️ Practical Examples

### Example 1: Save and Retrieve Project Plan

```javascript
// Save project plan
const saveProjectPlan = async (projectData) => {
  const response = await fetch('https://your-project.cloudfunctions.net/saveProjectPlan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(projectData)
  });
  
  return await response.json();
};

// Usage
const result = await saveProjectPlan({
  project_name: "E-commerce App",
  project_type: "webapp",
  complexity: "high",
  tech_stack: "React + Node.js + MongoDB",
  deadline_weeks: 12,
  user_id: "user123"
});

console.log('Project saved:', result.project_id);
console.log('File saved:', result.file_id);
console.log('Download URL:', result.download_url);
```

### Example 2: File Search and Filter

```javascript
// Search files by multiple criteria
const searchUserFiles = async (userId, searchCriteria) => {
  const { tags, contentType, dateFrom, dateTo } = searchCriteria;
  
  let q = query(
    collection(db, 'files'),
    where('user_id', '==', userId)
  );
  
  if (tags && tags.length > 0) {
    q = query(q, where('tags', 'array-contains-any', tags));
  }
  
  if (contentType) {
    q = query(q, where('content_type', '==', contentType));
  }
  
  if (dateFrom) {
    q = query(q, where('created_at', '>=', dateFrom));
  }
  
  if (dateTo) {
    q = query(q, where('created_at', '<=', dateTo));
  }
  
  q = query(q, orderBy('created_at', 'desc'));
  
  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};
```

### Example 3: Bulk File Operations

```javascript
// Bulk save multiple files
const bulkSaveFiles = async (files, userId) => {
  const batch = writeBatch(db);
  const results = [];
  
  files.forEach(file => {
    const docRef = doc(collection(db, 'files'));
    batch.set(docRef, {
      ...file,
      user_id: userId,
      created_at: serverTimestamp(),
      updated_at: serverTimestamp()
    });
    results.push({ id: docRef.id, filename: file.filename });
  });
  
  await batch.commit();
  return results;
};
```

## 🚀 Deployment and Testing

### Test Your Implementation

```bash
# Test file save endpoint
curl -X POST https://your-project.cloudfunctions.net/saveTextFile \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "test.txt",
    "content": "Hello, Firestore!",
    "user_id": "test-user",
    "tags": ["test", "example"]
  }'

# Test file download
curl "https://your-project.cloudfunctions.net/downloadFile?file_id=YOUR_FILE_ID" \
  -o downloaded_file.txt
```

### Monitor Performance

```javascript
// Add performance monitoring
const startTime = Date.now();
const result = await saveFile(fileData);
const endTime = Date.now();
console.log(`File save took ${endTime - startTime}ms`);
```

This comprehensive guide covers all aspects of creating queries, saving files to Firestore, and accessing them efficiently. Your existing Firebase setup provides a solid foundation for implementing these patterns.
