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
    autonomous,
    admin_escalation,
    api_pentesting,
    malware_analysis,
    continuous_forensics,
)

api_router = APIRouter()

api_router.include_router(forensics.router, prefix="/forensics", tags=["forensics"])
api_router.include_router(ai_analysis.router, prefix="/ai", tags=["ai"])
api_router.include_router(api_pentesting.router, prefix="/api-pentesting", tags=["api-pentesting"])
api_router.include_router(persistence.router, prefix="/persistence", tags=["persistence"])
api_router.include_router(stealth.router, prefix="/stealth", tags=["stealth"])
api_router.include_router(network_security.router, prefix="/network", tags=["network"])
api_router.include_router(ot_security.router, prefix="/ot", tags=["ot"])
api_router.include_router(c2.router, prefix="/c2", tags=["c2"])
api_router.include_router(task_manager.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(autonomous.router, prefix="/autonomous", tags=["autonomous"])
api_router.include_router(admin_escalation.router, prefix="/admin-escalation", tags=["admin-escalation"])
api_router.include_router(malware_analysis.router, prefix="/malware", tags=["malware"])
api_router.include_router(continuous_forensics.router, prefix="/continuous-forensics", tags=["continuous-forensics"])
