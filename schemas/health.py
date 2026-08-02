# schemas/health.py

from pydantic import BaseModel


# ==========================================================
# HEALTH RESPONSE SCHEMA
# ==========================================================

class HealthResponse(BaseModel):
    status: str