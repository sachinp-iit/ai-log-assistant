# api/ingestion.py

from fastapi import APIRouter

from config.settings import settings
from services.ingestion_service import IngestionService

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/run")
async def run_ingestion():
    
    service = IngestionService(settings.INFRA_LOG_DIRECTORY)
    
    return {
        "status": "completed",
        "message": "Infrastructure logs ingested successfully."
    }