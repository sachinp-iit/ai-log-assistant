# api/ingestion.py

from fastapi import APIRouter

from config.settings import settings
from services.ingestion_service import IngestionService

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/run")
async def run_ingestion():
    """Run the infrastructure log ingestion pipeline."""
    
    service = IngestionService(settings.INFRA_LOG_DIRECTORY)    
    service.run_ingestions()
    
    return {
        "status": "completed",
        "message": "Infrastructure logs ingested successfully."
    }