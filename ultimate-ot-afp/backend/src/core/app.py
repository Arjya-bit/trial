"""
FastAPI Application Factory
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import init_databases, close_databases
from ..api.v1.routers import api_router
from ..api.websocket.realtime import setup_websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 Starting Ultimate OT-AFP Platform...")
    await init_databases()
    print("✅ Databases initialized")
    yield
    # Shutdown
    print("🛑 Shutting down Ultimate OT-AFP Platform...")
    await close_databases()
    print("✅ Cleanup completed")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Ultimate Operational Technology Advanced Forensics Platform",
        version=settings.VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # GZip Middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    # Setup WebSocket
    setup_websocket(app)
    
    @app.get("/")
    async def root():
        return {
            "message": "Ultimate OT-AFP Platform API",
            "version": settings.VERSION,
            "status": "operational"
        }
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": settings.VERSION
        }
    
    return app
