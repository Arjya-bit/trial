"""
C2 (Command & Control) API Endpoints
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Optional, List
from ....modules.c2.c2_server import get_c2_server

router = APIRouter()


class ImplantRegistration(BaseModel):
    hostname: str
    ip_address: str
    os: str
    username: str
    privileges: str
    metadata: Dict = {}


class HeartbeatRequest(BaseModel):
    implant_id: str
    status_data: Dict


class TaskRequest(BaseModel):
    type: str
    command: str
    parameters: Dict = {}


class TaskResult(BaseModel):
    task_id: str
    result: Dict


@router.post("/register")
async def register_implant(implant: ImplantRegistration):
    """Register a new C2 implant"""
    try:
        c2 = get_c2_server()
        result = await c2.register_implant(implant.dict())
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/heartbeat")
async def heartbeat(request: HeartbeatRequest, api_key: str = Header(None)):
    """Process implant heartbeat"""
    try:
        c2 = get_c2_server()
        result = await c2.heartbeat(request.implant_id, request.status_data)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/implants/{implant_id}/tasks")
async def send_task(implant_id: str, task: TaskRequest):
    """Send task to implant"""
    try:
        c2 = get_c2_server()
        result = await c2.send_task(implant_id, task.dict())
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/implants/{implant_id}/tasks/{task_id}/results")
async def receive_task_result(implant_id: str, task_id: str, result: TaskResult):
    """Receive task result from implant"""
    try:
        c2 = get_c2_server()
        ack = await c2.receive_task_result(implant_id, task_id, result.result)
        return {"status": "success", "data": ack}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/implants")
async def get_implants(status: Optional[str] = None):
    """Get list of implants"""
    try:
        c2 = get_c2_server()
        implants = await c2.get_implants(status)
        return {"status": "success", "data": implants}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/implants/{implant_id}")
async def get_implant_details(implant_id: str):
    """Get detailed information about an implant"""
    try:
        c2 = get_c2_server()
        implant = await c2.get_implant_details(implant_id)
        
        if not implant:
            raise HTTPException(status_code=404, detail="Implant not found")
        
        return {"status": "success", "data": implant}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/implants/{implant_id}")
async def remove_implant(implant_id: str):
    """Remove/deactivate an implant"""
    try:
        c2 = get_c2_server()
        success = await c2.remove_implant(implant_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Implant not found")
        
        return {"status": "success", "message": "Implant removed"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
