# config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


# ==========================================================
# CONFIGURATION SETTING MODEL
# ==========================================================

class Settings(BaseSettings):
    
    # ==========================================================
    # FASTAPI APPLICATION
    # ==========================================================
    
    APP_NAME: str
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int
    DEBUG: bool
    
    
    # ==========================================================
    # OPENROUTER CONFIGURATION
    # ==========================================================
    
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_MODEL: str
    OPENROUTER_HEADER_HTTP_REFERER: str
    OPENROUTER_HEADER_HTTP_X_TITLE: str
    
    
    # ==========================================================
    # QDRANT VECTOR DATABASE
    # ==========================================================
    
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str
    
    
    # ==========================================================
    # EMBEDDING + RERANKING MODELS
    # ==========================================================
    
    EMBEDDING_MODEL: str
    RERANKER_MODEL: str
    
    
    # ==========================================================
    # LOG CHUNK PROCESSING
    # ==========================================================
    
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    TOP_K_RESULTS: int
    INGESTION_BATCH_SIZE: int
    MAX_CONCURRENT_BATCHES: int
    
    
    # ==========================================================
    # INFRA LOG DIRECTORY
    # ==========================================================
    
    INFRA_LOG_DIRECTORY: str
    
    
    # ==========================================================
    # LANGSMITH OBSERVABILITY
    # ==========================================================
    
    LANGSMITH_TRACING_V2: bool
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    
    
    # ==========================================================
    # LOGGING
    # ==========================================================
    
    LOG_LEVEL: str
    
    
    # ==========================================================
    # EMBEDDING CONFIGURAITON
    # ==========================================================
    
    EMBEDDING_DIMENSION: int
    
    
    # ==========================================================
    # PYDANTIC SETTINGS CONFIG
    # ==========================================================
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = True
    )
    
    
# ==========================================================
# GLOBAL SETTINGS INSTANCE
# ==========================================================

settings = Settings()