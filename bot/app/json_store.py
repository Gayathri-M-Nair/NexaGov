import json

def load_events_from_json(filepath: str = "data/kerala_schemes.json"):
    """Load schemes/events with error handling"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Handle different JSON structures
            if isinstance(data, dict):
                # Try common keys: kerala_schemes, events, schemes, data
                schemes = (data.get("kerala_schemes") or 
                          data.get("events") or 
                          data.get("schemes") or 
                          data.get("data") or [])
            elif isinstance(data, list):
                schemes = data
            else:
                schemes = []
            print(f"📄 Loaded {len(schemes)} schemes from JSON")
            return schemes
    except FileNotFoundError:
        print(f"⚠️ Schemes file not found: {filepath}")
        return []
    except Exception as e:
        print(f"❌ Error loading schemes: {e}")
        return []
