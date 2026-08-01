# main.py

from fastapi import FastAPI
from config.settings import settings
from dotenv import load_dotenv
import uvicorn


# ==========================================================
# LOAD ENVIRONMENT CONFIGURAITON
# ==========================================================

load_dotenv()


# ==========================================================
# FASTAPI APPLICATION INITIALIZATION
# ==========================================================

app = FastAPI(
    title = settings.APP_NAME,
    version = settings.APP_VERSION,
    debug = settings.DEBUG
)


# ==========================================================
# ROOT ENDPOINT
# ==========================================================

@app.get("/")
async def root():
    
    return {
        "message": "AI Log Assistant",
        "version": settings.APP_VERSION,
        "status": "healthy"
    }
    

# ==========================================================
# APPLICATION STARTUP EVENT
# ==========================================================

@app.on_event("startup")
async def startup_event():
    
    print("Application startup completed.")
    

# ==========================================================
# APPLICATION SHUTDOWN EVENT
# ==========================================================

@app.on_event("shutdown")
async def shutdown_event():
    
    print("Application shutdown completed.")