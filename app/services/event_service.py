from app.db.database import get_database
from app.schemas.event import EventIn


def ingest_event(event: EventIn) -> str:
    """
    Ingest an event into MongoDB.
    
    Args:
        event: Validated event data (EventIn schema)
        
    Returns:
        str: The inserted document ID as a string
    """
    db = get_database()
    event_dict = event.model_dump()
    result = db.events.insert_one(event_dict)
    return str(result.inserted_id)


def get_events(limit: int = 10, offset: int = 0):
    """
    Fetch events from MongoDB with pagination and sorting.
    
    Args:
        limit: Maximum number of events to return (default: 10)
        offset: Number of events to skip (default: 0)
        
    Returns:
        list: List of event dictionaries with _id converted to string.
              Returns empty list if no events are found.
    """
    db = get_database()
    # Query events sorted by timestamp descending (newest first)
    cursor = (
        db.events
        .find({})
        .sort("timestamp", -1)
        .skip(offset)
        .limit(limit)
    )

    events = []
    # Convert MongoDB ObjectId to string for JSON serialization
    for event in cursor:
        event["_id"] = str(event["_id"])
        events.append(event)

    return events

