from fastapi import HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError

from app.core.security import decode_access_token
from app.services.audit_service import log_audit_event

# Configure HTTPBearer to return 401 instead of 403 for missing tokens
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Dependency to validate JWT token and return current user context.
    
    Args:
        request: FastAPI Request object for accessing client information
        credentials: HTTP Bearer token credentials
        
    Returns:
        dict: User context with username and role
            {
                "username": str,
                "role": str
            }
        
    Raises:
        HTTPException: 401 with specific error message for:
            - Missing token
            - Expired token
            - Invalid token
    """
    # Handle missing token
    if credentials is None:
        # Log authentication failure
        log_audit_event(
            user="unknown",
            role="unknown",
            action="AUTHENTICATION_FAILED",
            resource=request.url.path,
            status="FAILURE",
            ip_address=request.client.host if request.client else "unknown",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Missing token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # Decode and validate token with specific error handling
    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError:
        # Log authentication failure (expired token)
        log_audit_event(
            user="unknown",
            role="unknown",
            action="AUTHENTICATION_FAILED",
            resource=request.url.path,
            status="FAILURE",
            ip_address=request.client.host if request.client else "unknown",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please login again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        # Log authentication failure (invalid token)
        log_audit_event(
            user="unknown",
            role="unknown",
            action="AUTHENTICATION_FAILED",
            resource=request.url.path,
            status="FAILURE",
            ip_address=request.client.host if request.client else "unknown",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate token payload structure
    username: str = payload.get("sub")
    if username is None:
        # Log authentication failure (invalid payload)
        log_audit_event(
            user="unknown",
            role="unknown",
            action="AUTHENTICATION_FAILED",
            resource=request.url.path,
            status="FAILURE",
            ip_address=request.client.host if request.client else "unknown",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    role: str = payload.get("role")
    
    return {
        "username": username,
        "role": role,
    }
