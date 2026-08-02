# api/routes.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Root"])
async def root():
    return {
        "application": "AI Log Assistant",
        "status": "running"
    }
    
    
@router.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy"
    }