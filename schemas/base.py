# schemas/base.py

from datetime import datetime
from pydantic import BaseModel, ConfigDict

# ==========================================================
# BASE RESPONSE SCHEMA
# ==========================================================

class BaseResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime = datetime.utcnow()
    
    model_config = ConfigDict(
        from_attributes=True
    )
    