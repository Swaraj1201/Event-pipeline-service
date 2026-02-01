from time import time
from fastapi import HTTPException, status

from app.services.audit_service import log_audit_event

# Rate limit configuration
RATE_LIMIT = 5  # Maximum number of requests
WINDOW_SECONDS = 60  # Time window in seconds (per minute)

# In-memory store for tracking requests
# Format: {ip_address: [timestamp1, timestamp2, ...]}
requests_store = {}


def check_rate_limit(key: str, resource: str = "unknown"):
    """
    Check if a request should be rate limited based on the provided key.
    
    Args:
        key: Unique identifier for rate limiting (typically IP address)
        resource: Resource/endpoint that was accessed (for audit logging)
        
    Raises:
        HTTPException: 429 Too Many Requests if rate limit is exceeded
    """
    current_time = time()
    window_start = current_time - WINDOW_SECONDS
    
    # Get request history for this key (IP address)
    history = requests_store.get(key, [])
    
    # Clean up old timestamps outside the current time window
    history = [t for t in history if t > window_start]
    
    # Check if rate limit is exceeded
    if len(history) >= RATE_LIMIT:
        # Log rate limit violation
        log_audit_event(
            user="anonymous",
            role="N/A",
            action="RATE_LIMIT_EXCEEDED",
            resource=resource,
            status="BLOCKED",
            ip_address=key,
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests, please try again later"
        )
    
    # Add current request timestamp
    history.append(current_time)
    requests_store[key] = history
