// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getFunctions } from "firebase/functions";

// Your web app's Firebase configuration
// IMPORTANT: Replace these placeholder values with your actual Firebase project configuration
const firebaseConfig = {
  "projectId": "your-project-id",
  "appId": "your-app-id",
  "storageBucket": "your-project-id.firebasestorage.app",
  "apiKey": "your-api-key-here",
  "authDomain": "your-project-id.firebaseapp.com",
  "measurementId": "your-measurement-id",
  "messagingSenderId": "your-messaging-sender-id"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const functions = getFunctions(app);

export { db, functions };
