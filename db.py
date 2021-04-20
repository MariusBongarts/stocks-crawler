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
  data["day"] = date.today().day
  data["month"] = date.today().month
  data["year"] = date.today().year
  day_string = date.today().day if date.today().day > 10 else f'0{date.today().day}'
  month_string = date.today().month if date.today().month > 10 else f'0{date.today().month}'
  date_id = f'{data["year"]}{month_string}{day_string}'
  db.collection(collection).document(date_id + data['id']).set(data)

