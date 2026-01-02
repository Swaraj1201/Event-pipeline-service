from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Event Pipeline Service"}


@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

