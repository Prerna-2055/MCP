const functions = require('firebase-functions');
const admin = require('firebase-admin');
const cors = require('cors')({ origin: true });

// Initialize Firestore (assuming admin is already initialized in index.js)
const db = admin.firestore();

// Cloud Function to save any text file to Firestore
exports.saveTextFile = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { filename, content, user_id, tags = [], is_public = false, metadata = {} } = req.body;
      
      if (!filename || !content) {
        return res.status(400).json({ error: 'Missing filename or content' });
      }

      // Validate file size (limit to 1MB for text files)
      const contentSize = Buffer.byteLength(content, 'utf8');
      if (contentSize > 1024 * 1024) {
        return res.status(400).json({ error: 'File too large. Maximum size is 1MB.' });
      }

      // Save file to Firestore
      const fileDoc = {
        filename,
        content,
        content_type: 'text/plain',
        size: contentSize,
        user_id: user_id || 'anonymous',
        tags: Array.isArray(tags) ? tags : [],
        is_public: Boolean(is_public),
        metadata: metadata || {},
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      };

      const docRef = await db.collection('files').add(fileDoc);

      res.json({
        id: docRef.id,
        message: 'File saved successfully',
        filename,
        size: contentSize,
        download_url: `${req.protocol}://${req.get('host')}/downloadFile?file_id=${docRef.id}`
      });

    } catch (error) {
      console.error('Error saving file:', error);
      res.status(500).json({ error: 'Failed to save file' });
    }
  });
});

// Cloud Function to download files from Firestore
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
      
      // Check if file is public or user has access
      // In production, you'd want proper authentication here
      
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

// Cloud Function to list user files
exports.listUserFiles = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { user_id, tags, limit = 20, page = 0 } = req.query;
      
      if (!user_id) {
        return res.status(400).json({ error: 'Missing user_id parameter' });
      }

      let query = db.collection('files')
        .where('user_id', '==', user_id);

      // Add tag filter if provided
      if (tags) {
        const tagArray = Array.isArray(tags) ? tags : tags.split(',');
        query = query.where('tags', 'array-contains-any', tagArray);
      }

      // Add ordering and pagination
      query = query.orderBy('created_at', 'desc')
        .limit(parseInt(limit))
        .offset(parseInt(page) * parseInt(limit));

      const snapshot = await query.get();
      
      const files = snapshot.docs.map(doc => {
        const data = doc.data();
        // Don't return content in list view for performance
        const { content, ...fileInfo } = data;
        return {
          id: doc.id,
          ...fileInfo,
          download_url: `${req.protocol}://${req.get('host')}/downloadFile?file_id=${doc.id}`
        };
      });

      res.json({
        files,
        total: files.length,
        page: parseInt(page),
        limit: parseInt(limit)
      });

    } catch (error) {
      console.error('Error listing files:', error);
      res.status(500).json({ error: 'Failed to list files' });
    }
  });
});

// Cloud Function to get file metadata without content
exports.getFileInfo = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { file_id } = req.query;
      
      if (!file_id) {
        return res.status(400).json({ error: 'Missing file_id parameter' });
      }

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

// Cloud Function to update file metadata
exports.updateFileMetadata = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { file_id, tags, is_public, metadata } = req.body;
      
      if (!file_id) {
        return res.status(400).json({ error: 'Missing file_id parameter' });
      }

      const updateData = {
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      };

      if (tags !== undefined) {
        updateData.tags = Array.isArray(tags) ? tags : [];
      }

      if (is_public !== undefined) {
        updateData.is_public = Boolean(is_public);
      }

      if (metadata !== undefined) {
        updateData.metadata = metadata;
      }

      await db.collection('files').doc(file_id).update(updateData);

      res.json({
        id: file_id,
        message: 'File metadata updated successfully'
      });

    } catch (error) {
      console.error('Error updating file metadata:', error);
      res.status(500).json({ error: 'Failed to update file metadata' });
    }
  });
});

// Cloud Function to delete a file
exports.deleteFile = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { file_id, user_id } = req.body;
      
      if (!file_id || !user_id) {
        return res.status(400).json({ error: 'Missing file_id or user_id parameter' });
      }

      // Get file to verify ownership
      const fileDoc = await db.collection('files').doc(file_id).get();
      
      if (!fileDoc.exists) {
        return res.status(404).json({ error: 'File not found' });
      }

      const fileData = fileDoc.data();
      
      // Verify user owns the file
      if (fileData.user_id !== user_id) {
        return res.status(403).json({ error: 'Unauthorized to delete this file' });
      }

      // Delete the file
      await db.collection('files').doc(file_id).delete();

      res.json({
        id: file_id,
        message: 'File deleted successfully'
      });

    } catch (error) {
      console.error('Error deleting file:', error);
      res.status(500).json({ error: 'Failed to delete file' });
    }
  });
});

// Cloud Function to search files
exports.searchFiles = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { 
        user_id, 
        search_term, 
        tags, 
        content_type, 
        date_from, 
        date_to,
        is_public,
        limit = 20 
      } = req.query;

      let query = db.collection('files');

      // Add user filter if provided
      if (user_id) {
        query = query.where('user_id', '==', user_id);
      }

      // Add public filter if specified
      if (is_public !== undefined) {
        query = query.where('is_public', '==', is_public === 'true');
      }

      // Add content type filter
      if (content_type) {
        query = query.where('content_type', '==', content_type);
      }

      // Add tag filter
      if (tags) {
        const tagArray = Array.isArray(tags) ? tags : tags.split(',');
        query = query.where('tags', 'array-contains-any', tagArray);
      }

      // Add date filters
      if (date_from) {
        query = query.where('created_at', '>=', new Date(date_from));
      }

      if (date_to) {
        query = query.where('created_at', '<=', new Date(date_to));
      }

      // Add ordering and limit
      query = query.orderBy('created_at', 'desc').limit(parseInt(limit));

      const snapshot = await query.get();
      
      let files = snapshot.docs.map(doc => {
        const data = doc.data();
        const { content, ...fileInfo } = data;
        return {
          id: doc.id,
          ...fileInfo,
          download_url: `${req.protocol}://${req.get('host')}/downloadFile?file_id=${doc.id}`
        };
      });

      // If search term is provided, filter by filename or content
      if (search_term) {
        const searchLower = search_term.toLowerCase();
        files = files.filter(file => 
          file.filename.toLowerCase().includes(searchLower) ||
          (file.metadata && file.metadata.description && 
           file.metadata.description.toLowerCase().includes(searchLower))
        );
      }

      res.json({
        files,
        total: files.length,
        search_term: search_term || null
      });

    } catch (error) {
      console.error('Error searching files:', error);
      res.status(500).json({ error: 'Failed to search files' });
    }
  });
});

// Cloud Function to bulk save files
exports.bulkSaveFiles = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    try {
      const { files, user_id } = req.body;
      
      if (!files || !Array.isArray(files) || files.length === 0) {
        return res.status(400).json({ error: 'Missing or invalid files array' });
      }

      if (!user_id) {
        return res.status(400).json({ error: 'Missing user_id' });
      }

      // Validate file count (limit to 10 files per batch)
      if (files.length > 10) {
        return res.status(400).json({ error: 'Maximum 10 files per batch' });
      }

      const batch = db.batch();
      const results = [];

      files.forEach(file => {
        if (!file.filename || !file.content) {
          throw new Error(`Invalid file: missing filename or content`);
        }

        const docRef = db.collection('files').doc();
        const fileDoc = {
          filename: file.filename,
          content: file.content,
          content_type: file.content_type || 'text/plain',
          size: Buffer.byteLength(file.content, 'utf8'),
          user_id,
          tags: file.tags || [],
          is_public: file.is_public || false,
          metadata: file.metadata || {},
          created_at: admin.firestore.FieldValue.serverTimestamp(),
          updated_at: admin.firestore.FieldValue.serverTimestamp()
        };

        batch.set(docRef, fileDoc);
        results.push({
          id: docRef.id,
          filename: file.filename,
          size: fileDoc.size
        });
      });

      await batch.commit();

      res.json({
        message: 'Files saved successfully',
        files: results,
        total: results.length
      });

    } catch (error) {
      console.error('Error bulk saving files:', error);
      res.status(500).json({ error: 'Failed to bulk save files' });
    }
  });
});
