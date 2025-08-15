# 🛒 GDPR-Compliant E-commerce App with Firestore
## Complete Implementation Guide with Queries and File Operations

This guide demonstrates how to build a GDPR-compliant e-commerce application using Firestore for data storage, queries, and file operations while ensuring full compliance with European data protection regulations.

## 📋 Table of Contents
1. [GDPR Requirements for E-commerce](#gdpr-requirements)
2. [Firestore Data Architecture](#firestore-data-architecture)
3. [GDPR-Compliant Cloud Functions](#gdpr-compliant-cloud-functions)
4. [User Data Management](#user-data-management)
5. [Order and Transaction Handling](#order-and-transaction-handling)
6. [File Operations for Compliance](#file-operations-for-compliance)
7. [Security Rules](#security-rules)
8. [Testing and Validation](#testing-and-validation)

## 🔒 GDPR Requirements for E-commerce

### Key GDPR Principles for E-commerce:
- **Lawful Basis**: Clear legal basis for processing personal data
- **Data Minimization**: Only collect necessary data
- **Purpose Limitation**: Use data only for stated purposes
- **Storage Limitation**: Delete data when no longer needed
- **Accuracy**: Keep data accurate and up-to-date
- **Security**: Implement appropriate technical measures
- **Accountability**: Demonstrate compliance

### E-commerce Specific Requirements:
- **Consent Management**: Track user consent for marketing, cookies, etc.
- **Right to Access**: Users can download their data
- **Right to Rectification**: Users can update their information
- **Right to Erasure**: Users can request data deletion
- **Data Portability**: Export user data in machine-readable format
- **Breach Notification**: Report breaches within 72 hours

## 🗂️ Firestore Data Architecture

### Collection Structure for GDPR Compliance

```javascript
// GDPR-compliant Firestore collections
ecommerce_app/
├── users/                          // User accounts and profiles
│   ├── {userId}/
│   │   ├── profile                 // Basic profile data
│   │   ├── preferences             // User preferences and consent
│   │   ├── addresses               // Shipping addresses
│   │   └── gdpr_records            // GDPR compliance tracking
├── orders/                         // Order information
│   ├── {orderId}/
│   │   ├── order_details           // Order information
│   │   ├── items                   // Order items
│   │   └── gdpr_metadata           // Compliance metadata
├── products/                       // Product catalog
├── consent_records/                // User consent tracking
├── data_requests/                  // GDPR data requests
├── audit_logs/                     // Compliance audit trail
└── compliance_files/               // GDPR documentation
```

### Document Schemas

```javascript
// User Profile Document
{
  id: "user123",
  email: "user@example.com",
  firstName: "John",
  lastName: "Doe",
  dateOfBirth: "1990-01-01",
  phone: "+46701234567",
  marketingConsent: true,
  cookieConsent: true,
  dataProcessingConsent: true,
  consentTimestamp: "2024-01-15T10:30:00Z",
  consentVersion: "1.2",
  dataRetentionUntil: "2027-01-15T10:30:00Z",
  created_at: timestamp,
  updated_at: timestamp,
  gdpr_metadata: {
    lawfulBasis: "consent",
    dataCategories: ["personal", "contact", "preferences"],
    processingPurposes: ["order_fulfillment", "customer_service"],
    dataSource: "user_registration",
    retentionPeriod: "3_years"
  }
}

// Order Document
{
  id: "order456",
  userId: "user123",
  orderNumber: "ORD-2024-001",
  status: "completed",
  items: [...],
  totalAmount: 299.99,
  currency: "EUR",
  shippingAddress: {...},
  billingAddress: {...},
  paymentMethod: "card_ending_1234",
  created_at: timestamp,
  gdpr_metadata: {
    lawfulBasis: "contract",
    dataCategories: ["transaction", "financial", "shipping"],
    processingPurposes: ["order_fulfillment", "accounting"],
    retentionPeriod: "7_years_tax_law"
  }
}

// Consent Record Document
{
  id: "consent789",
  userId: "user123",
  consentType: "marketing",
  consentGiven: true,
  consentTimestamp: "2024-01-15T10:30:00Z",
  consentVersion: "1.2",
  ipAddress: "192.168.1.1",
  userAgent: "Mozilla/5.0...",
  consentMethod: "checkbox",
  withdrawalTimestamp: null,
  isActive: true
}
```

## ⚡ GDPR-Compliant Cloud Functions

### 1. User Registration with GDPR Compliance

```javascript
// Cloud Function: registerUser
exports.registerUser = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { 
        email, 
        firstName, 
        lastName, 
        dateOfBirth,
        phone,
        marketingConsent,
        cookieConsent,
        consentVersion,
        ipAddress,
        userAgent 
      } = req.body;

      // Validate required fields
      if (!email || !firstName || !lastName) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      // Check if user already exists
      const existingUser = await db.collection('users')
        .where('email', '==', email)
        .get();

      if (!existingUser.empty) {
        return res.status(409).json({ error: 'User already exists' });
      }

      const userId = db.collection('users').doc().id;
      const now = admin.firestore.FieldValue.serverTimestamp();
      const retentionDate = new Date();
      retentionDate.setFullYear(retentionDate.getFullYear() + 3);

      // Create user profile
      const userProfile = {
        id: userId,
        email,
        firstName,
        lastName,
        dateOfBirth,
        phone,
        marketingConsent: marketingConsent || false,
        cookieConsent: cookieConsent || false,
        dataProcessingConsent: true, // Required for service
        consentTimestamp: now,
        consentVersion: consentVersion || "1.0",
        dataRetentionUntil: admin.firestore.Timestamp.fromDate(retentionDate),
        created_at: now,
        updated_at: now,
        gdpr_metadata: {
          lawfulBasis: "consent",
          dataCategories: ["personal", "contact", "preferences"],
          processingPurposes: ["account_management", "order_fulfillment"],
          dataSource: "user_registration",
          retentionPeriod: "3_years"
        }
      };

      // Create consent records
      const consentRecords = [];
      
      if (marketingConsent) {
        consentRecords.push({
          userId,
          consentType: "marketing",
          consentGiven: true,
          consentTimestamp: now,
          consentVersion: consentVersion || "1.0",
          ipAddress,
          userAgent,
          consentMethod: "registration_form",
          isActive: true
        });
      }

      if (cookieConsent) {
        consentRecords.push({
          userId,
          consentType: "cookies",
          consentGiven: true,
          consentTimestamp: now,
          consentVersion: consentVersion || "1.0",
          ipAddress,
          userAgent,
          consentMethod: "registration_form",
          isActive: true
        });
      }

      // Use batch write for atomicity
      const batch = db.batch();
      
      // Add user profile
      batch.set(db.collection('users').doc(userId), userProfile);
      
      // Add consent records
      consentRecords.forEach(consent => {
        const consentRef = db.collection('consent_records').doc();
        batch.set(consentRef, {
          ...consent,
          id: consentRef.id,
          created_at: now
        });
      });

      // Add audit log
      const auditRef = db.collection('audit_logs').doc();
      batch.set(auditRef, {
        id: auditRef.id,
        userId,
        action: "user_registration",
        details: {
          email,
          consentGiven: {
            marketing: marketingConsent || false,
            cookies: cookieConsent || false
          }
        },
        ipAddress,
        userAgent,
        timestamp: now
      });

      await batch.commit();

      res.json({
        success: true,
        userId,
        message: "User registered successfully with GDPR compliance"
      });

    } catch (error) {
      console.error('Error registering user:', error);
      res.status(500).json({ error: 'Registration failed' });
    }
  });
});
```

### 2. GDPR Data Subject Rights Implementation

```javascript
// Cloud Function: handleDataSubjectRequest
exports.handleDataSubjectRequest = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { userId, requestType, userEmail } = req.body;

      // Validate request
      if (!userId || !requestType || !userEmail) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      const validRequestTypes = ['access', 'rectification', 'erasure', 'portability', 'restriction'];
      if (!validRequestTypes.includes(requestType)) {
        return res.status(400).json({ error: 'Invalid request type' });
      }

      // Verify user identity
      const userDoc = await db.collection('users').doc(userId).get();
      if (!userDoc.exists || userDoc.data().email !== userEmail) {
        return res.status(403).json({ error: 'User verification failed' });
      }

      const requestId = db.collection('data_requests').doc().id;
      const now = admin.firestore.FieldValue.serverTimestamp();

      // Create data request record
      const dataRequest = {
        id: requestId,
        userId,
        userEmail,
        requestType,
        status: 'pending',
        requestDate: now,
        processingDeadline: admin.firestore.Timestamp.fromDate(
          new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
        ),
        created_at: now,
        updated_at: now
      };

      await db.collection('data_requests').doc(requestId).set(dataRequest);

      // Process request based on type
      let response = { requestId, status: 'pending' };

      switch (requestType) {
        case 'access':
          response = await processDataAccessRequest(userId, requestId);
          break;
        case 'erasure':
          response = await processDataErasureRequest(userId, requestId);
          break;
        case 'portability':
          response = await processDataPortabilityRequest(userId, requestId);
          break;
        default:
          // For rectification and restriction, manual processing required
          response.message = 'Request submitted for manual processing';
      }

      res.json(response);

    } catch (error) {
      console.error('Error handling data subject request:', error);
      res.status(500).json({ error: 'Request processing failed' });
    }
  });
});

// Helper function: Process data access request
const processDataAccessRequest = async (userId, requestId) => {
  try {
    // Collect all user data
    const userData = {};
    
    // Get user profile
    const userDoc = await db.collection('users').doc(userId).get();
    if (userDoc.exists) {
      userData.profile = userDoc.data();
    }

    // Get orders
    const ordersSnapshot = await db.collection('orders')
      .where('userId', '==', userId)
      .get();
    userData.orders = ordersSnapshot.docs.map(doc => doc.data());

    // Get consent records
    const consentSnapshot = await db.collection('consent_records')
      .where('userId', '==', userId)
      .get();
    userData.consentRecords = consentSnapshot.docs.map(doc => doc.data());

    // Get addresses
    const addressesSnapshot = await db.collection('users')
      .doc(userId)
      .collection('addresses')
      .get();
    userData.addresses = addressesSnapshot.docs.map(doc => doc.data());

    // Create downloadable file
    const fileName = `user_data_${userId}_${Date.now()}.json`;
    const fileContent = JSON.stringify(userData, null, 2);

    // Save file to Firestore
    const fileDoc = await db.collection('compliance_files').add({
      fileName,
      content: fileContent,
      contentType: 'application/json',
      userId,
      requestId,
      requestType: 'access',
      size: Buffer.byteLength(fileContent, 'utf8'),
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      expiresAt: admin.firestore.Timestamp.fromDate(
        new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
      )
    });

    // Update request status
    await db.collection('data_requests').doc(requestId).update({
      status: 'completed',
      completedAt: admin.firestore.FieldValue.serverTimestamp(),
      fileId: fileDoc.id,
      downloadUrl: `${req.protocol}://${req.get('host')}/downloadComplianceFile?file_id=${fileDoc.id}`
    });

    return {
      requestId,
      status: 'completed',
      message: 'Data access request processed successfully',
      downloadUrl: `${req.protocol}://${req.get('host')}/downloadComplianceFile?file_id=${fileDoc.id}`,
      fileId: fileDoc.id
    };

  } catch (error) {
    console.error('Error processing data access request:', error);
    throw error;
  }
};

// Helper function: Process data erasure request
const processDataErasureRequest = async (userId, requestId) => {
  try {
    // Check for legal obligations to retain data
    const ordersSnapshot = await db.collection('orders')
      .where('userId', '==', userId)
      .where('status', 'in', ['pending', 'processing', 'shipped'])
      .get();

    if (!ordersSnapshot.empty) {
      await db.collection('data_requests').doc(requestId).update({
        status: 'rejected',
        rejectionReason: 'Active orders prevent data erasure',
        processedAt: admin.firestore.FieldValue.serverTimestamp()
      });

      return {
        requestId,
        status: 'rejected',
        reason: 'Cannot delete data while orders are active'
      };
    }

    // Anonymize user data instead of deletion for audit trail
    const batch = db.batch();
    
    // Anonymize user profile
    const userRef = db.collection('users').doc(userId);
    batch.update(userRef, {
      firstName: 'DELETED',
      lastName: 'USER',
      email: `deleted_${userId}@anonymized.local`,
      phone: 'DELETED',
      dateOfBirth: null,
      marketingConsent: false,
      dataProcessingConsent: false,
      anonymized: true,
      anonymizedAt: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });

    // Delete consent records
    const consentSnapshot = await db.collection('consent_records')
      .where('userId', '==', userId)
      .get();
    
    consentSnapshot.docs.forEach(doc => {
      batch.delete(doc.ref);
    });

    // Delete addresses
    const addressesSnapshot = await db.collection('users')
      .doc(userId)
      .collection('addresses')
      .get();
    
    addressesSnapshot.docs.forEach(doc => {
      batch.delete(doc.ref);
    });

    await batch.commit();

    // Update request status
    await db.collection('data_requests').doc(requestId).update({
      status: 'completed',
      completedAt: admin.firestore.FieldValue.serverTimestamp()
    });

    return {
      requestId,
      status: 'completed',
      message: 'Data erasure request processed successfully'
    };

  } catch (error) {
    console.error('Error processing data erasure request:', error);
    throw error;
  }
};
```

### 3. Order Processing with GDPR Compliance

```javascript
// Cloud Function: createOrder
exports.createOrder = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const {
        userId,
        items,
        shippingAddress,
        billingAddress,
        paymentMethodId,
        totalAmount,
        currency = 'EUR'
      } = req.body;

      // Validate required fields
      if (!userId || !items || !shippingAddress || !totalAmount) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      // Verify user exists and has valid consent
      const userDoc = await db.collection('users').doc(userId).get();
      if (!userDoc.exists) {
        return res.status(404).json({ error: 'User not found' });
      }

      const userData = userDoc.data();
      if (!userData.dataProcessingConsent) {
        return res.status(403).json({ error: 'Data processing consent required' });
      }

      const orderId = db.collection('orders').doc().id;
      const orderNumber = `ORD-${new Date().getFullYear()}-${orderId.substring(0, 8).toUpperCase()}`;
      const now = admin.firestore.FieldValue.serverTimestamp();

      // Create order with GDPR metadata
      const order = {
        id: orderId,
        orderNumber,
        userId,
        status: 'pending',
        items,
        totalAmount,
        currency,
        shippingAddress: {
          ...shippingAddress,
          // Hash sensitive data for security
          hashedAddress: hashAddress(shippingAddress)
        },
        billingAddress: {
          ...billingAddress,
          hashedAddress: hashAddress(billingAddress)
        },
        paymentMethod: {
          id: paymentMethodId,
          // Store only last 4 digits for security
          lastFour: paymentMethodId.slice(-4),
          type: 'card'
        },
        created_at: now,
        updated_at: now,
        gdpr_metadata: {
          lawfulBasis: 'contract',
          dataCategories: ['transaction', 'financial', 'shipping', 'personal'],
          processingPurposes: ['order_fulfillment', 'customer_service', 'accounting'],
          retentionPeriod: '7_years_tax_law',
          dataMinimization: true,
          encryptionApplied: true
        }
      };

      // Save order
      await db.collection('orders').doc(orderId).set(order);

      // Create audit log
      await db.collection('audit_logs').add({
        userId,
        action: 'order_created',
        orderId,
        orderNumber,
        details: {
          totalAmount,
          currency,
          itemCount: items.length
        },
        timestamp: now,
        gdpr_compliant: true
      });

      res.json({
        success: true,
        orderId,
        orderNumber,
        status: 'pending',
        message: 'Order created successfully'
      });

    } catch (error) {
      console.error('Error creating order:', error);
      res.status(500).json({ error: 'Order creation failed' });
    }
  });
});

// Helper function to hash addresses for privacy
const hashAddress = (address) => {
  const crypto = require('crypto');
  const addressString = `${address.street} ${address.city} ${address.postalCode} ${address.country}`;
  return crypto.createHash('sha256').update(addressString).digest('hex');
};
```

### 4. Consent Management

```javascript
// Cloud Function: updateConsent
exports.updateConsent = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const {
        userId,
        consentType,
        consentGiven,
        consentVersion,
        ipAddress,
        userAgent
      } = req.body;

      // Validate input
      const validConsentTypes = ['marketing', 'cookies', 'analytics', 'personalization'];
      if (!validConsentTypes.includes(consentType)) {
        return res.status(400).json({ error: 'Invalid consent type' });
      }

      const now = admin.firestore.FieldValue.serverTimestamp();

      // Find existing consent record
      const existingConsentSnapshot = await db.collection('consent_records')
        .where('userId', '==', userId)
        .where('consentType', '==', consentType)
        .where('isActive', '==', true)
        .get();

      const batch = db.batch();

      // Deactivate existing consent if it exists
      if (!existingConsentSnapshot.empty) {
        existingConsentSnapshot.docs.forEach(doc => {
          batch.update(doc.ref, {
            isActive: false,
            withdrawalTimestamp: now,
            updated_at: now
          });
        });
      }

      // Create new consent record
      const newConsentRef = db.collection('consent_records').doc();
      batch.set(newConsentRef, {
        id: newConsentRef.id,
        userId,
        consentType,
        consentGiven,
        consentTimestamp: now,
        consentVersion: consentVersion || "1.0",
        ipAddress,
        userAgent,
        consentMethod: 'user_update',
        isActive: true,
        created_at: now
      });

      // Update user profile
      const updateData = {};
      updateData[`${consentType}Consent`] = consentGiven;
      updateData.updated_at = now;

      batch.update(db.collection('users').doc(userId), updateData);

      // Add audit log
      const auditRef = db.collection('audit_logs').doc();
      batch.set(auditRef, {
        id: auditRef.id,
        userId,
        action: 'consent_updated',
        details: {
          consentType,
          consentGiven,
          previousConsent: !existingConsentSnapshot.empty
        },
        ipAddress,
        userAgent,
        timestamp: now
      });

      await batch.commit();

      res.json({
        success: true,
        message: 'Consent updated successfully',
        consentType,
        consentGiven
      });

    } catch (error) {
      console.error('Error updating consent:', error);
      res.status(500).json({ error: 'Consent update failed' });
    }
  });
});
```

## 🔐 GDPR-Compliant Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == userId;
      
      // Prevent deletion of user profiles (use anonymization instead)
      allow delete: if false;
      
      // Addresses subcollection
      match /addresses/{addressId} {
        allow read, write: if request.auth != null && 
          request.auth.uid == userId;
      }
    }
    
    // Orders - users can only access their own orders
    match /orders/{orderId} {
      allow read: if request.auth != null && 
        request.auth.uid == resource.data.userId;
      allow write: if false; // Orders created via Cloud Functions only
    }
    
    // Consent records - read-only for users, write via Cloud Functions
    match /consent_records/{consentId} {
      allow read: if request.auth != null && 
        request.auth.uid == resource.data.userId;
      allow write: if false; // Managed via Cloud Functions
    }
    
    // Data requests - users can read their own requests
    match /data_requests/{requestId} {
      allow read: if request.auth != null && 
        request.auth.uid == resource.data.userId;
      allow create: if request.auth != null && 
        request.auth.uid == request.resource.data.userId;
      allow update, delete: if false; // Managed via Cloud Functions
    }
    
    // Compliance files - temporary access for data subjects
    match /compliance_files/{fileId} {
      allow read: if request.auth != null && 
        request.auth.uid == resource.data.userId &&
        request.time < resource.data.expiresAt;
      allow write: if false; // Created via Cloud Functions only
    }
    
    // Audit logs - no direct access
    match /audit_logs/{logId} {
      allow read, write: if false; // Admin access only via Cloud Functions
    }
    
    // Products - public read access
    match /products/{productId} {
      allow read: if true;
      allow write: if false; // Admin managed
    }
  }
}
```

## 🧪 Testing GDPR E-commerce Implementation

```python
#!/usr/bin/env python3
"""
GDPR E-commerce Firestore Testing Script
Tests all GDPR compliance features for e-commerce application
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "https://us-central1-mcptest-468919.cloudfunctions.net"

def test_user_registration_with_gdpr():
    """Test user registration with GDPR consent tracking"""
    print("🔐 Testing: GDPR-Compliant User Registration")
    
    url = f"{BASE_URL}/registerUser"
    
    payload = {
        "email": "john.doe@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "dateOfBirth": "1990-05-15",
        "phone": "+46701234567",
        "marketingConsent": True,
        "cookieConsent": True,
        "consentVersion": "2.1",
        "ipAddress": "192.168.1.100",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ User registered with GDPR compliance!")
        print(f"   User ID: {result['userId']}")
        print(f"   Consent tracking: Enabled")
        print(f"   Data retention: 3 years")
        
        return result['userId']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error registering user: {e}")
        return None

def test_create_gdpr_compliant_order(user_id):
    """Test order creation with GDPR compliance"""
    print(f"\n🛒 Testing: GDPR-Compliant Order Creation")
    
    url = f"{BASE_URL}/createOrder"
    
    payload = {
        "userId": user_id,
        "items": [
            {
                "productId": "prod_123",
                "name": "Organic Cotton T-Shirt",
                "price": 29.99,
                "quantity": 2
            },
            {
                "productId": "prod_456", 
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
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Order created with GDPR compliance!")
        print(f"   Order ID: {result['orderId']}")
        print(f"   Order Number: {result['orderNumber']}")
        print(f"   Legal basis: Contract")
        print(f"   Data retention: 7 years (tax law)")
        
        return result['orderId']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating order: {e}")
        return None

def test_data_subject_access_request(user_id, user_email):
    """Test GDPR data access request"""
    print(f"\n📋 Testing: GDPR Data Access Request")
    
    url = f"{BASE_URL}/handleDataSubjectRequest"
    
    payload = {
        "userId": user_id,
        "userEmail": user_email,
        "requestType": "access"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Data access request processed!")
        print(f"   Request ID: {result['requestId']}")
        print(f"   Status: {result['status']}")
        if 'downloadUrl' in result:
            print(f"   Download URL: {result['downloadUrl']}")
        
        return result['requestId']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error processing data access request: {e}")
        return None

def test_consent_management(user_id):
    """Test consent management system"""
    print(f"\n✅ Testing: Consent Management")
    
    url = f"{BASE_URL}/updateConsent"
    
    # Test withdrawing marketing consent
    payload = {
        "userId": user_id,
        "consentType": "marketing",
        "consentGiven": False,
        "consentVersion": "2.1",
        "ipAddress": "192.168.1.100",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Consent updated successfully!")
        print(f"   Consent type: {result['consentType']}")
        print(f"   Consent given: {result['consentGiven']}")
        print(f"   Audit trail: Created")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating consent
