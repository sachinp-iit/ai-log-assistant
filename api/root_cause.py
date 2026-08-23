# api/root_cause.py

from fastapi import APIRouter

from agents.root_cause_agent import analyze_root_cause

router = APIRouter(prefix = "/root-cause", tags = ["Root Cause"])

@router.post("/analyze")
async def analyze(anomaly: dict, related_logs: list[dict]):
    
    """Analyze potential anomaly root causes."""
    
    result = analyze_root_cause.invoke({
        "anomaly": anomaly,
        "related_logs": related_logs 
    })
    
    return {
        "status": "success",
        "analysis": result,
    }