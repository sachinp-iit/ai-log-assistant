# core/responses.py
from fastapi.responses import JSONResponse

# ==========================================================
# SUCCESS RESPONSES
# ==========================================================

def success_response(data=None, message: str = "Success", status_code: int = 200):
    
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data
        },        
    )
    

# ==========================================================
# ERROR RESPONSES
# ==========================================================
def error_response(message: str, status_code: int = 400):
    
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
        },  
    )