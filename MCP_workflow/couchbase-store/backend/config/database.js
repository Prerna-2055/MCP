const couchbase = require('couchbase');

let cluster;
let bucket;
let collection;

const connectToCouchbase = async () => {
  try {
    const connectionString = process.env.COUCHBASE_CONNECTION_STRING || 'couchbase://localhost';
    const username = process.env.COUCHBASE_USERNAME || 'Administrator';
    const password = process.env.COUCHBASE_PASSWORD || 'password';
    const bucketName = process.env.COUCHBASE_BUCKET || 'couchbase-store';

    // Connect to cluster
    cluster = await couchbase.connect(connectionString, {
      username: username,
      password: password,
    });

    // Get bucket reference
    bucket = cluster.bucket(bucketName);
    
    // Get default collection
    collection = bucket.defaultCollection();

    console.log('CouchBase connection established successfully');
    
    // Create indexes for better query performance
    await createIndexes();
    
    return { cluster, bucket, collection };
  } catch (error) {
    console.error('CouchBase connection error:', error);
    throw error;
  }
};

const createIndexes = async () => {
  try {
    const queryIndexManager = cluster.queryIndexes();
    
    // Create primary index if it doesn't exist
    try {
      await queryIndexManager.createPrimaryIndex(bucket.name);
      console.log('Primary index created');
    } catch (error) {
      if (!error.message.includes('already exists')) {
        console.error('Error creating primary index:', error);
      }
    }

    // Create secondary indexes for common queries
    const indexes = [
      {
        name: 'idx_type',
        fields: ['type'],
        bucketName: bucket.name
      },
      {
        name: 'idx_email',
        fields: ['email'],
        bucketName: bucket.name
      },
      {
        name: 'idx_category',
        fields: ['category'],
        bucketName: bucket.name
      },
      {
        name: 'idx_status',
        fields: ['status'],
        bucketName: bucket.name
      }
    ];

    for (const index of indexes) {
      try {
        await queryIndexManager.createIndex(index.bucketName, index.name, index.fields);
        console.log(`Index ${index.name} created`);
      } catch (error) {
        if (!error.message.includes('already exists')) {
          console.error(`Error creating index ${index.name}:`, error);
        }
      }
    }
  } catch (error) {
    console.error('Error creating indexes:', error);
  }
};

const getCluster = () => cluster;
const getBucket = () => bucket;
const getCollection = () => collection;

const closeConnection = async () => {
  if (cluster) {
    await cluster.close();
    console.log('CouchBase connection closed');
  }
};

module.exports = {
  connectToCouchbase,
  getCluster,
  getBucket,
  getCollection,
  closeConnection
};
