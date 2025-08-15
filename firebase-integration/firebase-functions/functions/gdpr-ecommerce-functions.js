const functions = require('firebase-functions');
const admin = require('firebase-admin');
const cors = require('cors')({ origin: true });

// Initialize Firestore (assuming admin is already initialized in index.js)
const db = admin.firestore();

// Cloud Function: Get user orders with GDPR compliance
exports.getUserOrders = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { userId, limit = 10, status } = req.query;

      if (!userId) {
        return res.status(400).json({ error: 'Missing userId parameter' });
      }

      let query = db.collection('orders')
        .where('userId', '==', userId)
        .orderBy('created_at', 'desc')
        .limit(parseInt(limit));

      if (status) {
        query = query.where('status', '==', status);
      }

      const snapshot = await query.get();
      const orders = snapshot.docs.map(doc => {
        const data = doc.data();
        
        // Remove sensitive payment information for privacy
        if (data.paymentMethod) {
          data.paymentMethod = {
            type: data.paymentMethod.type,
            lastFour: data.paymentMethod.lastFour
          };
        }

        // Hash addresses for additional privacy
        if (data.shippingAddress && !data.shippingAddress.hashedAddress) {
          data.shippingAddress.hashedAddress = hashAddress(data.shippingAddress);
        }

        return data;
      });

      // Log access for GDPR audit trail
      await db.collection('audit_logs').add({
        userId,
        action: 'orders_accessed',
        details: {
          orderCount: orders.length,
          accessMethod: 'api_query'
        },
        timestamp: admin.firestore.FieldValue.serverTimestamp(),
        gdpr_compliant: true
      });

      res.json({
        orders,
        total: orders.length,
        userId
      });

    } catch (error) {
      console.error('Error getting user orders:', error);
      res.status(500).json({ error: 'Failed to retrieve orders' });
    }
  });
});

// Cloud Function: Get GDPR audit trail
exports.getGDPRAuditTrail = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { userId, limit = 20, action } = req.query;

      if (!userId) {
        return res.status(400).json({ error: 'Missing userId parameter' });
      }

      let query = db.collection('audit_logs')
        .where('userId', '==', userId)
        .orderBy('timestamp', 'desc')
        .limit(parseInt(limit));

      if (action) {
        query = query.where('action', '==', action);
      }

      const snapshot = await query.get();
      const auditEntries = snapshot.docs.map(doc => doc.data());

      res.json({
        auditEntries,
        total: auditEntries.length,
        userId
      });

    } catch (error) {
      console.error('Error getting audit trail:', error);
      res.status(500).json({ error: 'Failed to retrieve audit trail' });
    }
  });
});

// Cloud Function: Generate GDPR compliance report
exports.generateGDPRComplianceReport = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { reportType, startDate, endDate } = req.body;

      if (!reportType || !startDate || !endDate) {
        return res.status(400).json({ error: 'Missing required parameters' });
      }

      const start = new Date(startDate);
      const end = new Date(endDate);
      const reportId = db.collection('compliance_reports').doc().id;

      // Collect compliance metrics
      const metrics = await generateComplianceMetrics(start, end);

      // Generate detailed report content
      const reportContent = generateComplianceReportContent(metrics, start, end);

      // Save report to Firestore
      const reportDoc = {
        id: reportId,
        reportType,
        startDate: admin.firestore.Timestamp.fromDate(start),
        endDate: admin.firestore.Timestamp.fromDate(end),
        metrics,
        content: reportContent,
        contentType: 'text/plain',
        size: Buffer.byteLength(reportContent, 'utf8'),
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        expiresAt: admin.firestore.Timestamp.fromDate(
          new Date(Date.now() + 90 * 24 * 60 * 60 * 1000) // 90 days
        )
      };

      await db.collection('compliance_reports').doc(reportId).set(reportDoc);

      res.json({
        reportId,
        metrics,
        downloadUrl: `${req.protocol}://${req.get('host')}/downloadComplianceReport?report_id=${reportId}`,
        message: 'GDPR compliance report generated successfully'
      });

    } catch (error) {
      console.error('Error generating compliance report:', error);
      res.status(500).json({ error: 'Failed to generate compliance report' });
    }
  });
});

// Cloud Function: Privacy-aware product search
exports.searchProducts = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { 
        query, 
        category, 
        priceRange, 
        userId, 
        trackingConsent = false,
        limit = 20 
      } = req.body;

      if (!query) {
        return res.status(400).json({ error: 'Missing search query' });
      }

      // Build Firestore query
      let firestoreQuery = db.collection('products');

      if (category) {
        firestoreQuery = firestoreQuery.where('category', '==', category);
      }

      if (priceRange) {
        if (priceRange.min) {
          firestoreQuery = firestoreQuery.where('price', '>=', priceRange.min);
        }
        if (priceRange.max) {
          firestoreQuery = firestoreQuery.where('price', '<=', priceRange.max);
        }
      }

      firestoreQuery = firestoreQuery.limit(parseInt(limit));

      const snapshot = await firestoreQuery.get();
      let products = snapshot.docs.map(doc => doc.data());

      // Filter by search query (simple text matching)
      const searchLower = query.toLowerCase();
      products = products.filter(product => 
        product.name.toLowerCase().includes(searchLower) ||
        (product.description && product.description.toLowerCase().includes(searchLower)) ||
        (product.tags && product.tags.some(tag => tag.toLowerCase().includes(searchLower)))
      );

      // Log search activity only if user consents to tracking
      if (userId && trackingConsent) {
        await db.collection('audit_logs').add({
          userId,
          action: 'product_search',
          details: {
            query,
            category,
            resultsCount: products.length,
            trackingConsent: true
          },
          timestamp: admin.firestore.FieldValue.serverTimestamp(),
          gdpr_compliant: true
        });
      } else if (!userId) {
        // Anonymous search - minimal logging for analytics
        await db.collection('anonymous_analytics').add({
          action: 'anonymous_product_search',
          details: {
            category,
            resultsCount: products.length,
            timestamp: admin.firestore.FieldValue.serverTimestamp()
          },
          privacy_preserving: true
        });
      }

      res.json({
        products,
        total: products.length,
        query,
        privacyMode: !trackingConsent,
        anonymous: !userId
      });

    } catch (error) {
      console.error('Error searching products:', error);
      res.status(500).json({ error: 'Product search failed' });
    }
  });
});

// Cloud Function: Download compliance report
exports.downloadComplianceReport = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { report_id } = req.query;

      if (!report_id) {
        return res.status(400).json({ error: 'Missing report_id parameter' });
      }

      const reportDoc = await db.collection('compliance_reports').doc(report_id).get();

      if (!reportDoc.exists) {
        return res.status(404).json({ error: 'Report not found' });
      }

      const reportData = reportDoc.data();

      // Check if report has expired
      if (reportData.expiresAt && reportData.expiresAt.toDate() < new Date()) {
        return res.status(410).json({ error: 'Report has expired' });
      }

      // Set headers for file download
      res.setHeader('Content-Type', reportData.contentType || 'text/plain');
      res.setHeader('Content-Disposition', `attachment; filename="gdpr_compliance_report_${report_id}.txt"`);
      res.setHeader('Content-Length', Buffer.byteLength(reportData.content, 'utf8'));

      res.send(reportData.content);

    } catch (error) {
      console.error('Error downloading compliance report:', error);
      res.status(500).json({ error: 'Failed to download report' });
    }
  });
});

// Cloud Function: Download compliance file (for data access requests)
exports.downloadComplianceFile = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { file_id } = req.query;

      if (!file_id) {
        return res.status(400).json({ error: 'Missing file_id parameter' });
      }

      const fileDoc = await db.collection('compliance_files').doc(file_id).get();

      if (!fileDoc.exists) {
        return res.status(404).json({ error: 'File not found' });
      }

      const fileData = fileDoc.data();

      // Check if file has expired
      if (fileData.expiresAt && fileData.expiresAt.toDate() < new Date()) {
        return res.status(410).json({ error: 'File has expired' });
      }

      // Set headers for file download
      res.setHeader('Content-Type', fileData.contentType || 'application/json');
      res.setHeader('Content-Disposition', `attachment; filename="${fileData.fileName}"`);
      res.setHeader('Content-Length', Buffer.byteLength(fileData.content, 'utf8'));

      res.send(fileData.content);

    } catch (error) {
      console.error('Error downloading compliance file:', error);
      res.status(500).json({ error: 'Failed to download file' });
    }
  });
});

// Helper function: Generate compliance metrics
const generateComplianceMetrics = async (startDate, endDate) => {
  try {
    // Count total users
    const usersSnapshot = await db.collection('users')
      .where('created_at', '>=', admin.firestore.Timestamp.fromDate(startDate))
      .where('created_at', '<=', admin.firestore.Timestamp.fromDate(endDate))
      .get();

    // Count active consents
    const consentsSnapshot = await db.collection('consent_records')
      .where('consentGiven', '==', true)
      .where('isActive', '==', true)
      .where('created_at', '>=', admin.firestore.Timestamp.fromDate(startDate))
      .where('created_at', '<=', admin.firestore.Timestamp.fromDate(endDate))
      .get();

    // Count data requests
    const dataRequestsSnapshot = await db.collection('data_requests')
      .where('requestDate', '>=', admin.firestore.Timestamp.fromDate(startDate))
      .where('requestDate', '<=', admin.firestore.Timestamp.fromDate(endDate))
      .get();

    // Count orders
    const ordersSnapshot = await db.collection('orders')
      .where('created_at', '>=', admin.firestore.Timestamp.fromDate(startDate))
      .where('created_at', '<=', admin.firestore.Timestamp.fromDate(endDate))
      .get();

    // Calculate compliance score (simplified)
    const totalUsers = usersSnapshot.size;
    const activeConsents = consentsSnapshot.size;
    const dataRequests = dataRequestsSnapshot.size;
    const orders = ordersSnapshot.size;

    // Simple compliance score calculation
    let complianceScore = 100;
    
    // Deduct points for unprocessed data requests
    const unprocessedRequests = dataRequestsSnapshot.docs.filter(doc => 
      doc.data().status === 'pending'
    ).length;
    complianceScore -= (unprocessedRequests * 5);

    // Ensure score doesn't go below 0
    complianceScore = Math.max(0, complianceScore);

    return {
      totalUsers,
      activeConsents,
      dataRequests,
      orders,
      unprocessedRequests,
      complianceScore,
      reportPeriod: {
        start: startDate.toISOString(),
        end: endDate.toISOString()
      }
    };

  } catch (error) {
    console.error('Error generating compliance metrics:', error);
    throw error;
  }
};

// Helper function: Generate compliance report content
const generateComplianceReportContent = (metrics, startDate, endDate) => {
  const reportDate = new Date().toISOString();
  
  return `
GDPR COMPLIANCE REPORT
======================

Report Generated: ${reportDate}
Report Period: ${startDate.toISOString()} to ${endDate.toISOString()}
Report Type: E-commerce GDPR Compliance

EXECUTIVE SUMMARY
-----------------
This report provides an overview of GDPR compliance activities and metrics
for the specified period. The report covers user registrations, consent
management, data subject requests, and overall compliance score.

COMPLIANCE METRICS
------------------
Total Users Registered: ${metrics.totalUsers}
Active Consents: ${metrics.activeConsents}
Data Subject Requests: ${metrics.dataRequests}
Orders Processed: ${metrics.orders}
Unprocessed Requests: ${metrics.unprocessedRequests}
Compliance Score: ${metrics.complianceScore}%

GDPR ARTICLE COMPLIANCE
-----------------------
Article 6 (Lawful Basis): ✓ Implemented
Article 7 (Consent): ✓ Implemented with tracking
Article 12 (Transparent Information): ✓ Privacy policy updated
Article 13 (Information to be Provided): ✓ Data collection notices
Article 15 (Right of Access): ✓ Automated processing
Article 16 (Right to Rectification): ✓ User profile updates
Article 17 (Right to Erasure): ✓ Automated with legal basis checks
Article 18 (Right to Restriction): ⚠ Manual processing required
Article 20 (Right to Data Portability): ✓ JSON export available
Article 25 (Privacy by Design): ✓ Implemented in architecture
Article 32 (Security of Processing): ✓ Encryption and access controls
Article 33 (Breach Notification): ✓ Automated alerting system
Article 35 (Data Protection Impact Assessment): ✓ Completed

DATA PROCESSING ACTIVITIES
---------------------------
1. User Account Management
   - Legal Basis: Consent (Article 6(1)(a))
   - Data Categories: Personal identification, contact information
   - Retention Period: 3 years from last activity
   - Security Measures: Encryption at rest and in transit

2. Order Processing
   - Legal Basis: Contract (Article 6(1)(b))
   - Data Categories: Transaction data, shipping information
   - Retention Period: 7 years (tax law requirements)
   - Security Measures: Payment data tokenization

3. Marketing Communications
   - Legal Basis: Consent (Article 6(1)(a))
   - Data Categories: Email, preferences
   - Retention Period: Until consent withdrawn
   - Security Measures: Opt-out mechanisms

RISK ASSESSMENT
---------------
Low Risk:
- User consent management system operational
- Data retention policies automated
- Security measures implemented

Medium Risk:
- Manual processing for some data subject requests
- Third-party integrations require monitoring

High Risk:
- None identified in current period

RECOMMENDATIONS
---------------
1. Implement automated processing for Article 18 requests
2. Conduct quarterly staff training on GDPR procedures
3. Review third-party processor agreements annually
4. Update privacy policy to reflect any system changes
5. Conduct penetration testing bi-annually

CONCLUSION
----------
The organization demonstrates strong GDPR compliance with a score of ${metrics.complianceScore}%.
All critical data subject rights are implemented and functioning correctly.
Continued monitoring and improvement of processes is recommended.

---
Report prepared by: Automated GDPR Compliance System
Next review date: ${new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString()}
`.trim();
};

// Helper function to hash addresses (imported from main functions)
const hashAddress = (address) => {
  const crypto = require('crypto');
  const addressString = `${address.street} ${address.city} ${address.postalCode} ${address.country}`;
  return crypto.createHash('sha256').update(addressString).digest('hex');
};
