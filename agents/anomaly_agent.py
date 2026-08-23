# agents/anomaly_agent.py

from langchain_core.tools import tool
from sklearn.ensemble import IsolationForest
import pandas as pd

from config.settings import settings

@tool
def detect_anomalies(data: list[dict]) -> list[dict]:
    """Detect infrastructure metric anomalies."""
    
    dataframe = pd.DataFrame(data)
    
    features = [
        "cpu_usage",
        "memory_usage",
        "network_traffic",
        "power_consumption",
        "execution_time",
        "energy_efficiency",
    ]
    
    model = IsolationForest(
        n_estimators = 200,
        contamination="auto",
        random_state = 42,
        n_jobs = -1,
    )
    
    dataframe["anomaly_prediction"] = model.fit_predict(
        dataframe[features]
    )
    
    return dataframe[
        dataframe["anomaly_prediction"] == -1
    ].to_dict(orient="records")