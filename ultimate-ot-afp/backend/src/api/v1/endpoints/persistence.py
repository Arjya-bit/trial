"""
Persistence API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class PersistenceRequest(BaseModel):
    method: str  # service, registry, scheduled_task, wmi
    name: str
    command: str
    auto_start: bool = True


@router.post("/install")
async def install_persistence(request: PersistenceRequest):
    """Install persistence mechanism"""
    try:
        # Persistence installation logic
        return {
            "status": "success",
            "message": f"Persistence installed: {request.method}",
            "details": {
                "method": request.method,
                "name": request.name,
                "installed": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mechanisms")
async def get_persistence_mechanisms():
    """Get installed persistence mechanisms"""
    return {
        "status": "success",
        "data": []
    }


@router.delete("/mechanisms/{mechanism_id}")
async def remove_persistence(mechanism_id: str):
    """Remove persistence mechanism"""
    return {
        "status": "success",
        "message": "Persistence mechanism removed"
    }
