from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, verify_password
from app.schemas.user import TokenResponse, UserLogin

router = APIRouter()

# Mock user for learning purposes (no database yet)
# In production, this would be stored in a database
# Pre-computed bcrypt hash for the mock user password
MOCK_USER = {
    "username": "admin",
    "hashed_password": "$2b$12$mcimxB/MCj0rkALmv4c07ea/pUj7IeWI/ZfkNI2.GpP1k2TSWui.y",
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
    # Validate username
    if credentials.username != MOCK_USER["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    # Validate password
    if not verify_password(credentials.password, MOCK_USER["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": credentials.username})
    
    return TokenResponse(access_token=access_token, token_type="bearer")
