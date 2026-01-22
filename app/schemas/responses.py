from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response schema."""
    message: str
    data: T


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    message: str
    details: Optional[dict[str, Any]] = None

