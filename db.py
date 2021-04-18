import firebase_admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import sys
from dotenv import load_dotenv
load_dotenv()
import os

firebase_config = os.environ['FIREBASE_SDK']


firebase_config = json.loads(firebase_config)


cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
db = firestore.client()

def write(collection, data):
  print(data)
  db.collection(collection).document(data['id']).set(data)

