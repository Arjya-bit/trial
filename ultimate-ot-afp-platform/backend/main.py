#!/usr/bin/env python3
"""
Ultimate OT-AFP Platform - Backend Main Application
Comprehensive Operational Technology - Advanced Forensics Platform
"""

import os
import sys
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import core modules
from src.core.app import create_application
from src.core.config import settings
from src.core.security import setup_security
from src.database.redis_client import RedisClient
from src.database.elasticsearch_client import ElasticsearchClient

# Import module routers
from src.api.v1.routers import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backend.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global clients for cleanup
redis_client = None
es_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global redis_client, es_client

    logger.info("Starting Ultimate OT-AFP Platform Backend...")

    # Initialize Redis client
    try:
        redis_client = RedisClient()
        await redis_client.connect()
        logger.info("Redis client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Redis client: {e}")

    # Initialize Elasticsearch client
    try:
        es_client = ElasticsearchClient()
        await es_client.connect()
        logger.info("Elasticsearch client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Elasticsearch client: {e}")

    # Initialize AI models
    try:
        from src.modules.ai_model.model_downloader import ModelDownloader
        model_downloader = ModelDownloader()
        await model_downloader.initialize_models()
        logger.info("AI models initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI models: {e}")

    yield

    # Cleanup
    logger.info("Shutting down Ultimate OT-AFP Platform Backend...")

    if redis_client:
        await redis_client.disconnect()
    if es_client:
        await es_client.disconnect()

# Create FastAPI application
app = create_application()

# Add lifespan manager
app.router.lifespan_context = lifespan

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
if settings.ALLOWED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Ultimate OT-AFP Platform",
        "version": "1.0.0",
        "description": "Comprehensive Operational Technology - Advanced Forensics Platform",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time(),
        "services": {
            "redis": "connected" if redis_client and await redis_client.ping() else "disconnected",
            "elasticsearch": "connected" if es_client and await es_client.ping() else "disconnected"
        }
    }

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    return response

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_id": "INTERNAL_ERROR"}
    )

if __name__ == "__main__":
    # Run the application
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True
    )