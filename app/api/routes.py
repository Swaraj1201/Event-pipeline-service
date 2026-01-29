from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.schemas.event import EventIn
from app.schemas.responses import SuccessResponse
from app.services.event_service import get_events, ingest_event

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Dependency to validate JWT token and return current user.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        str: Username from token
        
    Raises:
        HTTPException: 401 if token is invalid or missing
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return username


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
    current_user: str = Depends(get_current_user),
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
    current_user: str = Depends(get_current_user),
):
    event_id = ingest_event(event)
    return SuccessResponse(
        message="Event created successfully",
        data={"event_id": event_id},
    )

