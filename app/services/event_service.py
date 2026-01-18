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

