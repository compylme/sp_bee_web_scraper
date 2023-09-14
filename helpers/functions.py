from google.cloud import firestore

db = firestore.Client(project = "spelling-bee-web-scraper")
def insert_letters_db(collection, payload, document_id):
    return db.collection(collection).document(document_id).set(payload)


def remove_spaces(string):
    return string.replace(" ", "")