import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
cred=credentials.Certificate(os.getcwd()+'\\src\\database_connection\\cs300-project-firebase-adminsdk-z5mzh-43da7b3a43.json')
firebase_admin.initialize_app(cred)
db=firestore.client()
obj1={
  "Name":"Mike",
  "Age":100,
  "Net worth":100000
}
obj2={
  "Nmae":"Tony",
  "Age":10,
  "New worth":100000
}
data=[obj1,obj2]
