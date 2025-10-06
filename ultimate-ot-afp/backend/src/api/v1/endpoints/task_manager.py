"""
Task Manager API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from ....modules.task_manager.process_monitor import ProcessMonitor

router = APIRouter()


@router.get("/processes")
async def get_processes():
    """Get all running processes"""
    try:
        monitor = ProcessMonitor()
        processes = await monitor.get_all_processes()
        return {"status": "success", "data": processes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/processes/{pid}")
async def get_process_details(pid: int):
    """Get detailed information about a process"""
    try:
        monitor = ProcessMonitor()
        details = await monitor.get_process_details(pid)
        
        if not details:
            raise HTTPException(status_code=404, detail="Process not found")
        
        return {"status": "success", "data": details}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/processes/{pid}")
async def kill_process(pid: int, force: bool = False):
    """Kill a process"""
    try:
        monitor = ProcessMonitor()
        success = await monitor.kill_process(pid, force)
        
        if not success:
            raise HTTPException(status_code=404, detail="Process not found")
        
        return {"status": "success", "message": "Process terminated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/processes/analyze/suspicious")
async def get_suspicious_processes():
    """Get list of suspicious processes"""
    try:
        monitor = ProcessMonitor()
        suspicious = await monitor.analyze_suspicious_processes()
        return {"status": "success", "data": suspicious}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system/stats")
async def get_system_stats():
    """Get system statistics"""
    try:
        monitor = ProcessMonitor()
        stats = await monitor.get_system_stats()
        return {"status": "success", "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
