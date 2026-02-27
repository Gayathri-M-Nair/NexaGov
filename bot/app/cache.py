# Lightweight in-memory cache with size limits
EVENT_CACHE = []
EVENT_INDEX = {}
MAX_EVENTS = 100  # Limit number of cached events

def load_event_cache(events):
    """
    Load events into memory with size limit.
    """
    EVENT_CACHE.clear()
    
    # Limit to MAX_EVENTS
    limited_events = events[:MAX_EVENTS] if len(events) > MAX_EVENTS else events
    EVENT_CACHE.extend(limited_events)

    EVENT_INDEX.clear()
    EVENT_INDEX.update({
        event["event_name"].lower(): event
        for event in limited_events
        if event.get("event_name")
    })
    
    print(f"📦 Cached {len(EVENT_CACHE)} events (limit: {MAX_EVENTS})")

def get_event_by_name(name: str):
    """
    Fast O(1) lookup by event name.
    """
    return EVENT_INDEX.get(name.lower())
