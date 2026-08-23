# agents/root_cause_agent.py

from langchain_core.tools import tool

@tool
def analyze_root_cause(anomaly: dict, related_logs = list[dict]) -> dict:
    """Analyze infrastructure metrics and related logs."""
    
    causes = []
    
    metrics = {
        "cpu_usage": anomaly.get("cpu_usage"),
        "memory_usage": anomaly.get("memory_usage"),
        "network_traffic": anomaly.get("network_traffic"),
        "power_consumption": anomaly.get("power_consumption"),
        "execution_time": anomaly.get("execution_time"),
    }
    
    for metric, value in metrics.items():
        if value is not None:
            causes.append({
                "metric": metric,
                "value": value,
            })
            
    return {
        "anomaly": anomaly,
        "potential_causes": causes,
        "related_logs": related_logs
    }