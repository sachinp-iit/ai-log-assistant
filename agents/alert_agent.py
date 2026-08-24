# agents/alert_agent.py

from langchain_core.tools import tool

@tool
def generate_alert(anomaly:dict, severity: str = "high") -> dict:
    """Generate a structured infrastructure anomaly alert."""
    
    return {
        "alert": True,
        "severity": severity,
        "anomaly": anomaly,
        "message": "Infrastructure anomaly detected.",
    }