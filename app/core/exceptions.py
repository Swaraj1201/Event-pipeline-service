from fastapi import HTTPException, status


class APIException(HTTPException):
    """Base exception class for API errors."""
    
    def __init__(self, message: str, status_code: int):
        super().__init__(status_code=status_code, detail=message)


class EventNotFoundException(APIException):
    """Exception raised when an event is not found."""
    
    def __init__(self):
        super().__init__(
            message="Event not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

