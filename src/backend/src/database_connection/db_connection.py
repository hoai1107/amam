import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth as auth_admin
import os
import pymongo
from pathlib import Path
import pyrebase

#cred=credentials.Certificate(os.getcwd()+'\\src\\database_connection\\cs300-project-firebase-adminsdk-z5mzh-43da7b3a43.json')
cred=credentials.Certificate(os.path.join(os.path.join(Path(__file__).parents[1],'database_connection','cs300-project-firebase-adminsdk-z5mzh-43da7b3a43.json')))
firebase_admin.initialize_app(cred)
firestore=firestore.client()

firebaseConfig = {
  "apiKey": "AIzaSyA2UriO3yX8eygs2GGc44IPjWgnoQgPcUU",
  "authDomain": "cs300-project.firebaseapp.com",
  "projectId": "cs300-project",
  "databaseURL": "https://cs300-project-default-rtdb.firebaseio.com/",
  "storageBucket": "cs300-project.appspot.com",
  "messagingSenderId": "772462018723",
  "appId": "1:772462018723:web:f9d44024c0d105d162bf16",
  "measurementId": "G-PK0MK3ZPD2"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

client = pymongo.MongoClient("mongodb+srv://root:zi2kQbzaJQ5LS4jD@cluster0.evfi3hk.mongodb.net/?retryWrites=true&w=majority")
mongodb = client["ANAM"]
