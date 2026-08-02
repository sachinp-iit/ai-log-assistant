# core/telemetry.py

from logging import Logger, basicConfig, getLogger

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from config.settings import settings


# ==========================================================
# LOGGER
# ==========================================================

logger: Logger = getLogger(settings.APP_NAME)


# ==========================================================
# CONFIGURATION PYTHON LOGGING
# ==========================================================

def configure_logging() -> None:
    """
    Configure application logging.
    """
    
    basicConfig(
        level = settings.OTEL_LOG_LEVEL,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        )
    )
    
    LoggingInstrumentor().instrument(
        set_logging_format=True,
    )
    
    
# ==========================================================
# CONFIGURE OPENTELEMETRY
# ==========================================================

def configure_telemetry() -> None:
    """
    Configure OpenTelemetry tracing.
    """
    
    resource = Resource.create(
        {
            "service.name": settings.OTEL_SERVICE_NAME,
            "service.version": settings.OTEL_SERVICE_VERSION,
            "deployment.environment": "development"
        }
    )
    
    trace_provider = TracerProvider(
        resource = resource
    )
    
    span_exporter = OTLPSpanExporter(
        endpoint=settings.OTEL_EXPORT_OTLP_ENDPOINT
    )
    
    span_processor = BatchSpanProcessor(
        span_exporter,
    )
    
    trace_provider.add_span_processor(
        span_processor,
    )
    
    trace.set_tracer_provider(
        trace_provider,
    )
    

# ==========================================================
# INSTRUMENT APPLICATION
# ==========================================================

def instrument_app(app) -> None:
    """
    Instrument FastAPI and HTTP clients.
    """
    
    FastAPIInstrumentor.instrument_app(app)
    HTTPXClientInstrumentor().instrument()
    
    
# ==========================================================
# INITIALIZE TELEMETRY
# ==========================================================

def initialize_telemetry(app) -> None:
    """
    Initialize logging, tracing and instrumentation.
    """
    
    configure_logging()
    configure_telemetry()
    instrument_app(app)
    logger.info("OpenTelemetry initialized successfully.")
    