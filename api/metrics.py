# api/metrics.py

from fastapi import APIRouter

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/overview")
async def metrics_overview():
    """Return infrastructure metrics overview"""
    
    return {
        "status": "success",
        "message": "Metrics endpoint ready."
    }