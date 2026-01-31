from fastapi import APIRouter, Depends, Query, Request, status

from app.core.authorization import require_any_role, require_role
from app.schemas.event import EventIn
from app.schemas.responses import SuccessResponse
from app.services.audit_service import log_audit_event
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
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict = Depends(require_any_role("admin", "analyst")),
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
async def create_event(
    event: EventIn,
    request: Request,
    current_user: dict = Depends(require_role("admin")),
):
    event_id = ingest_event(event)
    
    # Log successful event creation
    log_audit_event(
        user=current_user["username"],
        role=current_user["role"],
        action="CREATE_EVENT",
        resource="events",
        status="SUCCESS",
        ip_address=request.client.host or "unknown",
    )
    
    return SuccessResponse(
        message="Event created successfully",
        data={"event_id": event_id},
    )

