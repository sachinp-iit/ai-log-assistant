# api/anomaly.py

from fastapi import APIRouter, HTTPException

from agents.anomaly_agent import detect_anomalies

router = APIRouter(prefix = "/anomaly", tags=["Anomaly"])

@router.post("/detect")
async def detect(data: list[dict]):
    """Detect anomalies from infrastructure metrics."""
    
    try:
        result = detect_anomalies.invoke({
            "data": data,
        })
        
        return {
            "status": "success",
            "anomalies": result,
        }
        
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail = str(exc)
        ) from exc