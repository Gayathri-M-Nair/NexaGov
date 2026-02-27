import firebase_admin
from firebase_admin import credentials, firestore

def init_firestore():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_service_account.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()


def fetch_events_from_firestore():
    print("⚠️ Falling back to Firebase Firestore...")
    db = init_firestore()

    docs = db.collection("events").stream()
    events = []

    for doc in docs:
        data = doc.to_dict()
        events.append({
            "event_name": data.get("event_name"),
            "venue": data.get("venue"),
            "time": data.get("time"),
            "date": data.get("date"),
            "details": data.get("details"),
            "coordinator": data.get("coordinator"),
            "fest": data.get("fest"),
            "slots": data.get("slots"),
            "poster": data.get("poster"),
            "amount": data.get("amount"),
            "phone_number":doc.get("phone_number"),
            "category": data.get("category")
        })

    print(f"✅ Loaded {len(events)} events from Firestore")
    return events
