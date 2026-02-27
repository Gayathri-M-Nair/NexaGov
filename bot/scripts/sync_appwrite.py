import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from firestore_fallback import fetch_events_from_firestore

load_dotenv()

APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")

DATABASE_ID = "6948d5240015a19ea05a"
COLLECTION_ID = "events"

OUTPUT_FILE = "data/events.json"

URL = f"{APPWRITE_ENDPOINT}/databases/{DATABASE_ID}/collections/{COLLECTION_ID}/documents"

HEADERS = {
    "X-Appwrite-Project": APPWRITE_PROJECT_ID,
    "X-Appwrite-Key": APPWRITE_API_KEY
}


def fetch_from_appwrite():
    print("Fetching events from Appwrite (REST API)...")

    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    data = response.json()
    documents = data.get("documents", [])

    events = []
    for doc in documents:
        # Convert date from ISO format to DD/MM/YYYY
        raw_date = doc.get("date")
        formatted_date = raw_date
        if raw_date:
            try:
                # Parse ISO 8601 format: "2026-06-02T00:00:00.000+00:00"
                dt = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                # Convert to DD/MM/YYYY
                formatted_date = dt.strftime("%d/%m/%Y")
            except Exception as e:
                print(f"⚠️ Could not parse date '{raw_date}': {e}")
                formatted_date = raw_date  # Keep original if parsing fails
        
        events.append({
            "event_name": doc.get("event_name"),
            "venue": doc.get("venue"),
            "time": doc.get("time"),
            "date": formatted_date,
            "details": doc.get("details"),
            "coordinator": doc.get("coordinator"),
            "fest": doc.get("fest"),
            "slots": doc.get("slots"),
            "poster": doc.get("poster"),
            "amount": doc.get("amount"),
            "phone_number":doc.get("phone_number"),
            "category": doc.get("category")
        })

    return events


def sync_events():
    try:
        events = fetch_from_appwrite()
        if not events:
            raise ValueError("No events returned from Appwrite")

        source = "Appwrite"

    except Exception as e:
        print(f"❌ Appwrite failed: {e}")
        events = fetch_events_from_firestore()
        source = "Firestore"

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

    print(f"✅ Synced {len(events)} events from {source} into {OUTPUT_FILE}")


if __name__ == "__main__":
    sync_events()
