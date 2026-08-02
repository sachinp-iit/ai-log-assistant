# core/logger.py

from logging import Logger, getLogger
from config.settings import settings

# ==========================================================
# LOGGER
# ==========================================================

logger: Logger = getLogger(settings.APP_NAME)