from firebase_admin import firestore, credentials
import firebase_admin
import pytz
import datetime

cred = credentials.Certificate('service-account-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
def insert_letters_db(collection_name, payload, document_id):
    try:
        db = firestore.Client()
        collection = db.collection(collection_name)
        document_ref = collection.document(document_id)
        document_ref.set(payload)
        print("Data inserted successfully into Firestore")
    except Exception as e:
        print("An error occurred while inserting data into Firestore:", str(e))


def remove_spaces(string):
    return string.replace(" ", "")


class myTimezones:
    
    def anchorageTime():
        usEastTimezone = pytz.timezone('America/Anchorage')
        current_date = datetime.datetime.now(usEastTimezone)
        formatted_time = current_date.strftime("%Y/%m/%d")
        formatted_date = str(formatted_time).replace("-", "/")

        return formatted_date
