from fastapi import APIRouter, Query

from app.schemas.event import EventIn
from app.services.event_service import get_events, ingest_event

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Event Pipeline Service"}


@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


@router.get("/events", tags=["Events"])
async def list_events(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return get_events(limit=limit, offset=offset)


@router.post("/events", tags=["Events"])
async def create_event(event: EventIn):
    event_id = ingest_event(event)
    return {"event_id": event_id}

