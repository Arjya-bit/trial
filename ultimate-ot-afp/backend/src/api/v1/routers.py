from fastapi import APIRouter, Depends

from src.core.security import verify_api_key
from src.api.v1.endpoints import (
    forensics,
    ai_analysis,
    persistence,
    stealth,
    network_security,
    ot_security,
    c2,
    task_manager,
    autonomous,
)

api_router = APIRouter(dependencies=[Depends(verify_api_key)])

api_router.include_router(forensics.router, prefix="/forensics", tags=["forensics"])
api_router.include_router(ai_analysis.router, prefix="/ai", tags=["ai"])
api_router.include_router(persistence.router, prefix="/persistence", tags=["persistence"])
api_router.include_router(stealth.router, prefix="/stealth", tags=["stealth"])
api_router.include_router(network_security.router, prefix="/network", tags=["network"])
api_router.include_router(ot_security.router, prefix="/ot", tags=["ot"])
api_router.include_router(c2.router, prefix="/c2", tags=["c2"])
api_router.include_router(task_manager.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(autonomous.router, prefix="/autonomous", tags=["autonomous"])
