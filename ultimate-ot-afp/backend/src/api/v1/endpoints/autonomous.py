"""
Autonomous Operations API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from ....modules.autonomous.auto_executor import get_auto_executor

router = APIRouter()


class TaskConfig(BaseModel):
    name: str
    trigger_type: str
    trigger_config: Dict
    enabled: bool = True


@router.post("/start")
async def start_autonomous_engine():
    """Start autonomous execution engine"""
    try:
        executor = get_auto_executor()
        await executor.start()
        return {"status": "success", "message": "Autonomous engine started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_autonomous_engine():
    """Stop autonomous execution engine"""
    try:
        executor = get_auto_executor()
        await executor.stop()
        return {"status": "success", "message": "Autonomous engine stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get status of an autonomous task"""
    try:
        executor = get_auto_executor()
        status = await executor.get_task_status(task_id)
        return {"status": "success", "data": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/{task_id}/enable")
async def enable_task(task_id: str):
    """Enable an autonomous task"""
    try:
        executor = get_auto_executor()
        await executor.enable_task(task_id)
        return {"status": "success", "message": "Task enabled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/{task_id}/disable")
async def disable_task(task_id: str):
    """Disable an autonomous task"""
    try:
        executor = get_auto_executor()
        await executor.disable_task(task_id)
        return {"status": "success", "message": "Task disabled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs")
async def get_execution_log(limit: int = 100):
    """Get autonomous execution log"""
    try:
        executor = get_auto_executor()
        logs = await executor.get_execution_log(limit)
        return {"status": "success", "data": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
