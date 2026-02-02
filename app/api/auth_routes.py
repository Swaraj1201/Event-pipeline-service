from fastapi import APIRouter, HTTPException, Request, status

from app.core.rate_limiter import check_rate_limit
from app.core.security import create_access_token, generate_refresh_token, verify_password
from app.schemas.user import RefreshTokenRequest, TokenResponse, UserLogin

router = APIRouter()

# Mock users for learning purposes (no database yet)
# In production, this would be stored in a database
# Pre-computed bcrypt hashes for the mock user passwords
MOCK_USERS = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$mcimxB/MCj0rkALmv4c07ea/pUj7IeWI/ZfkNI2.GpP1k2TSWui.y",
        "role": "admin",
    },
    "analyst": {
        "username": "analyst",
        "hashed_password": "$2b$12$r.chJHeCOT4S6zV0Fk7bN.d3wQKyPUjPBwjskegydRjRE5sctln92",
        "role": "analyst",
    },
}

# Mock refresh token store (no database yet)
# In production, this would be stored in a database with expiration
# Maps refresh_token -> username
REFRESH_TOKENS = {}


@router.post(
    "/login",
    summary="Authenticate user",
    description="Authenticate a user with username and password. Returns JWT access token and refresh token. Rate limited to prevent brute-force attacks.",
    tags=["Authentication"],
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def login(credentials: UserLogin, request: Request):
    """
    Authenticate user and return JWT access token.
    
    Args:
        credentials: User login credentials (username and password)
        
    Returns:
        TokenResponse: JWT access token and token type
        
    Raises:
        HTTPException: 401 if credentials are invalid
        HTTPException: 429 if rate limit is exceeded
    """
    # Check rate limit
    check_rate_limit(
        request.client.host if request.client else "unknown",
        resource="auth"
    )
    
    # Look up user in mock store
    user = MOCK_USERS.get(credentials.username)
    if user is None:
        # Use generic message to prevent username enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    # Validate password using bcrypt
    if not verify_password(credentials.password, user["hashed_password"]):
        # Use generic message to prevent username enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": credentials.username,
            "role": user["role"],
        }
    )
    
    # Generate refresh token
    refresh_token = generate_refresh_token()
    
    # Store refresh token (mock store)
    REFRESH_TOKENS[refresh_token] = credentials.username
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Refresh an expired access token using a valid refresh token. Returns a new access token and refresh token (token rotation). Rate limited to prevent abuse.",
    tags=["Authentication"],
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def refresh_token(token_request: RefreshTokenRequest, request: Request):
    """
    Refresh access token using a valid refresh token.
    
    Args:
        token_request: Refresh token request containing the refresh token
        request: FastAPI Request object for accessing client information
        
    Returns:
        TokenResponse: New access token and refresh token
        
    Raises:
        HTTPException: 401 if refresh token is invalid or expired
        HTTPException: 429 if rate limit is exceeded
    """
    # Check rate limit
    check_rate_limit(
        request.client.host if request.client else "unknown",
        resource="auth"
    )
    
    # Validate refresh token
    username = REFRESH_TOKENS.get(token_request.refresh_token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    # Get user information
    user = MOCK_USERS.get(username)
    if user is None:
        # User no longer exists, remove invalid refresh token
        REFRESH_TOKENS.pop(token_request.refresh_token, None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Generate new access token
    access_token = create_access_token(
        data={
            "sub": username,
            "role": user["role"],
        }
    )
    
    # Generate new refresh token (token rotation for security)
    new_refresh_token = generate_refresh_token()
    
    # Rotate tokens: remove old and store new to prevent token reuse
    REFRESH_TOKENS.pop(token_request.refresh_token, None)
    REFRESH_TOKENS[new_refresh_token] = username
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )
