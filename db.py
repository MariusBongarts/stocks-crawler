import firebase_admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import sys
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import date

firebase_config = os.environ['FIREBASE_SDK']


firebase_config = json.loads(firebase_config)


cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
db = firestore.client()

def write(collection, data):
  date_id = f'{date.today().year}{date.today().month}{date.today().day}'
  data["day"] = date.today().day
  data["month"] = date.today().month
  data["year"] = date.today().year
  db.collection(collection).document(date_id + data['id']).set(data)

