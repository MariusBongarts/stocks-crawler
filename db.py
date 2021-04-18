import firebase_admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from dotenv import load_dotenv
load_dotenv()
import os


firebase_config = y = json.loads(os.environ['FIREBASE_SDK'])
print(firebase_config)
if firebase_config is not None:
  with open('firebase-sdk-test.json', 'w') as f:
    json.dump(firebase_config, f)


cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def write(collection, data):
  print(data)
  db.collection(collection).document(data['id']).set(data)

