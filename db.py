import firebase_admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebase-sdk-prod.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def write(collection, data):
  print(data)
  db.collection(collection).document(data['id']).set(data)

