from fastapi import APIRouter, Query, status

from app.schemas.event import EventIn
from app.schemas.responses import SuccessResponse
from app.services.event_service import get_events, ingest_event

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Event Pipeline Service"}


@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


@router.get(
    "/events",
    tags=["Events"],
    response_model=SuccessResponse,
)
def list_events(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    events = get_events(limit=limit, offset=offset)
    return SuccessResponse(
        message="Events fetched successfully",
        data=events,
    )


@router.post(
    "/events",
    tags=["Events"],
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[dict],
)
async def create_event(event: EventIn):
    event_id = ingest_event(event)
    return SuccessResponse(
        message="Event created successfully",
        data={"event_id": event_id},
    )

