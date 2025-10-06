"""
V1 API Router for Ultimate OT-AFP Platform
"""

from fastapi import APIRouter

from .endpoints import (
    forensics, ai_analysis, network_security, ot_security,
    task_manager, autonomous, c2, stealth, persistence
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(forensics.router, prefix="/forensics", tags=["Forensics"])
api_router.include_router(ai_analysis.router, prefix="/ai", tags=["AI Analysis"])
api_router.include_router(network_security.router, prefix="/network", tags=["Network Security"])
api_router.include_router(ot_security.router, prefix="/ot", tags=["OT Security"])
api_router.include_router(task_manager.router, prefix="/tasks", tags=["Task Manager"])
api_router.include_router(autonomous.router, prefix="/autonomous", tags=["Autonomous Operations"])
api_router.include_router(c2.router, prefix="/c2", tags=["Command & Control"])
api_router.include_router(stealth.router, prefix="/stealth", tags=["Stealth Operations"])
api_router.include_router(persistence.router, prefix="/persistence", tags=["Persistence Engine"])