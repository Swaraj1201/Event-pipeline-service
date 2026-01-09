from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import get_settings

_client: Optional[MongoClient] = None


def get_database() -> Database:
    """Get MongoDB database instance."""
    global _client
    
    settings = get_settings()
    
    if _client is None:
        _client = MongoClient(settings.mongo_uri)
    
    return _client.get_database(settings.mongo_db_name)


def close_database() -> None:
    """Close MongoDB connection."""
    global _client
    
    if _client is not None:
        _client.close()
        _client = None

