from datetime import datetime
from pydantic import BaseModel, Field


class EventIn(BaseModel):
    source: str
    event_type: str
    payload: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)

