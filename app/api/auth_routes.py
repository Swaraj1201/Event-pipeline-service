from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, verify_password
from app.schemas.user import TokenResponse, UserLogin

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


@router.post(
    "/auth/login",
    tags=["Authentication"],
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT access token.
    
    Args:
        credentials: User login credentials (username and password)
        
    Returns:
        TokenResponse: JWT access token and token type
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Look up user
    user = MOCK_USERS.get(credentials.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    # Validate password
    if not verify_password(credentials.password, user["hashed_password"]):
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
    
    return TokenResponse(access_token=access_token, token_type="bearer")
