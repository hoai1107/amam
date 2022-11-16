'''// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA2UriO3yX8eygs2GGc44IPjWgnoQgPcUU",
  authDomain: "cs300-project.firebaseapp.com",
  projectId: "cs300-project",
  storageBucket: "cs300-project.appspot.com",
  messagingSenderId: "772462018723",
  appId: "1:772462018723:web:f9d44024c0d105d162bf16",
  measurementId: "G-PK0MK3ZPD2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);'''
import firebase_admin
cred_obj=firebase_admin.credentials.Certificate('...')