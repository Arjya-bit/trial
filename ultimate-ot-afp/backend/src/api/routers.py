"""
Main API Router for Ultimate OT-AFP Platform
"""

from fastapi import APIRouter
from .v1.routers import api_router as v1_router

# Main API router
api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")

# Health check
@api_router.get("/health")
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy", "service": "Ultimate OT-AFP API"}