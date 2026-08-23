# api/search.py

from fastapi import APIRouter

from services.retrieval_service import RetrievalService

router = APIRouter(prefix ="/search", tags = ["Search"])

@router.get("/")
async def search(query: str, limit: int | None = None):
    """Search infrastructure logs."""
    
    service = RetrievalService()
    
    results = service.search(
        query = query,
        limit = limit,
    )
    
    return {
        "query": query,
        "results": results
    }