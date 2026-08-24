# api/alert.py

from fastapi import APIRouter
from agents.alert_agent import generate_alert

router = APIRouter(prefix="/alert", tags=["Alert"])

@router.post("/generate")
async def generate(anomaly: dict, severity: str = "high"):
    """Generate an infrastructure anomaly alert"""
    
    result = generate_alert.invoke({
        "anomaly": anomaly,
        "severity": severity
    })
    
    return {
        "status": "success",
        "alert": result
    }