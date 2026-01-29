from pydantic import BaseModel


class UserLogin(BaseModel):
    """Schema for user login request."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
