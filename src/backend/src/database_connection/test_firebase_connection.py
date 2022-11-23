# This is just for testing the endpoints and will be deleted in the future
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyAqFS-ecMT6oJ4Dcf5dD4sAFNVUJflnLJo",
  "authDomain": "mama-e0162.firebaseapp.com",
  "databaseURL": "https://mama-e0162-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "mama-e0162",
  "storageBucket": "mama-e0162.appspot.com",
  "messagingSenderId": "500222370268",
  "appId": "1:500222370268:web:d51134f7d382c09c5bef19",
  "measurementId": "G-J2VSVV19E3"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()
