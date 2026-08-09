# main.py

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from api.routes import router
import uvicorn

from config.settings import settings
from core.telemetry import initialize_telemetry
from core.exceptions import register_exception_handlers

from api.ingestion import router as ingestion_router
from api.chat import router as chat_router


# ==========================================================
# LOAD ENVIRONMENT CONFIGURAITON
# ==========================================================

load_dotenv()

# ==========================================================
# APPLICATION LIFESPAN
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """

    # Startup
    print("Starting AI Log Assistant...")
    initialize_telemetry(app)

    yield

    # Shutdown
    print("Shutting down AI Log Assistant...")
    

# ==========================================================
# FASTAPI APPLICATION
# ==========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# ==========================================================
# APPLICATION CONFIGURATION SETTINGS
# ==========================================================

app.include_router(router)
app.include_router(ingestion_router)
app.include_router(chat_router)

register_exception_handlers(app)

# ==========================================================
# ROOT ENDPOINT
# ==========================================================

@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


# ==========================================================
# HEALTH CHECK ENDPOINT
# ==========================================================

@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
    }


# ==========================================================
# APPLICATION ENTRYPOINT
# ==========================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
    )