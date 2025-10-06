"""
Core FastAPI application factory
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
from contextlib import asynccontextmanager
from typing import Callable

from .config import settings
from .security import get_current_user
from ..api.v1.routers import api_router
from ..database.database import init_database

logger = logging.getLogger(__name__)

def create_app(lifespan: Callable = None) -> FastAPI:
    """
    Create and configure FastAPI application
    """
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="Ultimate Operational Technology - Advanced Forensics Platform",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Add middleware
    add_middleware(app)
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    
    # Add exception handlers
    add_exception_handlers(app)
    
    # Add startup and shutdown events
    add_events(app)
    
    return app

def add_middleware(app: FastAPI):
    """Add middleware to FastAPI app"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # GZip middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Custom security middleware
    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

def add_exception_handlers(app: FastAPI):
    """Add custom exception handlers"""
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

def add_events(app: FastAPI):
    """Add startup and shutdown events"""
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize application on startup"""
        logger.info("Initializing Ultimate OT-AFP Platform...")
        
        # Initialize database
        await init_database()
        
        logger.info("Platform initialized successfully!")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("Shutting down Ultimate OT-AFP Platform...")

# Health check endpoint
def add_health_check(app: FastAPI):
    """Add health check endpoint"""
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.VERSION}