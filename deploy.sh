#!/bin/bash

echo "🔥 Firebase Deployment Script for Prompt Context Server"
echo "======================================================"

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first:"
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ Prerequisites check complete"

# Navigate to firebase integration directory
cd firebase-integration

echo "📦 Installing dependencies..."
cd firebase-functions/functions
npm install

echo "🔐 Logging into Firebase..."
cd ../..
firebase login

echo "🚀 Initializing Firebase project..."
firebase init

echo "📤 Deploying to Firebase..."
firebase deploy

echo "✅ Deployment complete!"
echo ""
echo "🎉 Your Firebase Functions are now live!"
echo "📋 Next steps:"
echo "   1. Copy the function URLs from the deployment output"
echo "   2. Update your Lovable project with the Firebase config"
echo "   3. Copy the components from firebase-ready-components/"
echo ""
