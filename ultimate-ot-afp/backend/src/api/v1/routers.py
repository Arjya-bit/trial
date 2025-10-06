"""
API Router Configuration
Aggregates all API endpoints
"""
from fastapi import APIRouter
from .endpoints import (
    forensics,
    ai_analysis,
    persistence,
    stealth,
    network_security,
    ot_security,
    c2,
    task_manager,
    autonomous
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    forensics.router,
    prefix="/forensics",
    tags=["forensics"]
)

api_router.include_router(
    ai_analysis.router,
    prefix="/ai",
    tags=["ai-analysis"]
)

api_router.include_router(
    persistence.router,
    prefix="/persistence",
    tags=["persistence"]
)

api_router.include_router(
    stealth.router,
    prefix="/stealth",
    tags=["stealth"]
)

api_router.include_router(
    network_security.router,
    prefix="/network",
    tags=["network-security"]
)

api_router.include_router(
    ot_security.router,
    prefix="/ot-security",
    tags=["ot-security"]
)

api_router.include_router(
    c2.router,
    prefix="/c2",
    tags=["command-control"]
)

api_router.include_router(
    task_manager.router,
    prefix="/task-manager",
    tags=["task-manager"]
)

api_router.include_router(
    autonomous.router,
    prefix="/autonomous",
    tags=["autonomous"]
)
