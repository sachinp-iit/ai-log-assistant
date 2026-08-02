# dependencies/container.py

from functools import lru_cache
from config.settings import settings, Settings


# ==========================================================
# SETTINGS DEPENDENCY
# ==========================================================

@lru_cache
def get_settings() -> Settings:
    """
    Returns the application settings singleton.
    """
    
    return settings
    