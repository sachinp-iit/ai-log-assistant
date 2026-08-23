# agents/summary_agent.py

from langchain_core.tools import tool


@tool
def summarize_incident(anomaly:dict, root_cause: dict) -> str:
    """Create a concise infrastructure incident summary."""
    
    metric_summary = ", ".join(
        f"{key}={value}"
        for key, value in anomaly.items()
        if key != "anomaly_prediction"
    )
    
    causes = root_cause.get("potential_causes", [])
    
    cause_summary = ", ".join(
        f"{item['metric']}={item['value']}"
        for item in causes
    )
    
    return (
        f"Incident metrics: {metric_summary}. "
        f"Potential causes: {cause_summary}."
    )