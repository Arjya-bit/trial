"""
FastAPI application factory for Ultimate OT-AFP Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog

from .config import settings


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application
    """

    # Configure structured logging
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Create FastAPI application
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    if settings.ALLOWED_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add trusted host middleware for production
    if settings.ENVIRONMENT == "production" and settings.ALLOWED_HOSTS:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS
        )

    # Add security headers middleware
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request, call_next):
        logger = structlog.get_logger("api")
        logger.info(
            "Request started",
            method=request.method,
            url=str(request.url.path),
            client=request.client.host if request.client else "unknown"
        )

        response = await call_next(request)

        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url.path),
            status_code=response.status_code
        )

        return response

    return app