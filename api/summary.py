# api/summary.py

from fastapi import APIRouter

from agents.summary_agent import summarize_incident

router = APIRouter(prefix = "/summary", tags=["Summary"])

@router.post("/incident")
async def summarize(anomaly: dict, root_cause: dict):
    
    """Generate an incident summary."""
    
    result = summarize_incident.invoke({
        "anomaly": anomaly,
        "root_cause": root_cause
    })
    
    return {
        "status": "success",
        "summary": result,
    }