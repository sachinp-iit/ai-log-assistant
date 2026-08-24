# agents/anomaly_agent.py

import pandas as pd
from langchain_core.tools import tool
from sklearn.ensemble import IsolationForest


# ==========================================================
# ANOMALY DETECTION
# ==========================================================

@tool
def detect_anomalies(data: list[dict]) -> list[dict]:
    """
    Detect infrastructure anomalies using numeric metrics.
    """

    dataframe = pd.DataFrame(data)

    features = [
        "cpu_usage",
        "memory_usage",
        "network_traffic",
        "power_consumption",
        "execution_time",
        "energy_efficiency",
    ]

    # Validate required features.
    missing = [
        column
        for column in features
        if column not in dataframe.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required features: {missing}"
        )

    # Convert metrics to numeric values.
    # Invalid or missing values become NaN.
    dataframe[features] = dataframe[features].apply(
        pd.to_numeric,
        errors="coerce",
    )

    # Remove records that cannot be used for ML.
    dataframe = dataframe.dropna(
        subset=features
    )

    if dataframe.empty:
        raise ValueError(
            "No valid numeric records available for anomaly detection."
        )

    # Train anomaly detection model.
    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1,
    )

    dataframe["anomaly_prediction"] = model.fit_predict(
        dataframe[features]
    )

    # Return detected anomalies.
    return dataframe[
        dataframe["anomaly_prediction"] == -1
    ].to_dict(orient="records")