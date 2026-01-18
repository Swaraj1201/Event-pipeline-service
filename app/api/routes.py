from fastapi import APIRouter

from app.schemas.event import EventIn
from app.services.event_service import ingest_event

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Event Pipeline Service"}


@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


@router.post("/events", tags=["Events"])
async def create_event(event: EventIn):
    event_id = ingest_event(event)
    return {"event_id": event_id}

