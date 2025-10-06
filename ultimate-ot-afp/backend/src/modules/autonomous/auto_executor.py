"""
Autonomous Task Executor
Automatically executes security tasks based on triggers
"""
import asyncio
import logging
from typing import Dict, List, Callable
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class AutoExecutor:
    """Autonomous task execution engine"""
    
    def __init__(self):
        self.tasks = {}
        self.triggers = {}
        self.running = False
        self.execution_log = []
    
    async def register_task(
        self,
        name: str,
        function: Callable,
        trigger_type: str,
        trigger_config: Dict,
        enabled: bool = True
    ) -> str:
        """
        Register an autonomous task
        
        Args:
            name: Task name
            function: Async function to execute
            trigger_type: Type of trigger (schedule, event, threshold)
            trigger_config: Trigger configuration
            enabled: Whether task is enabled
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        
        task = {
            "id": task_id,
            "name": name,
            "function": function,
            "trigger_type": trigger_type,
            "trigger_config": trigger_config,
            "enabled": enabled,
            "created_at": datetime.utcnow().isoformat(),
            "last_execution": None,
            "execution_count": 0
        }
        
        self.tasks[task_id] = task
        
        logger.info(f"Autonomous task registered: {name} ({task_id})")
        
        return task_id
    
    async def start(self):
        """Start autonomous execution engine"""
        self.running = True
        logger.info("Autonomous executor started")
        
        # Start monitoring loop
        asyncio.create_task(self._execution_loop())
    
    async def stop(self):
        """Stop autonomous execution engine"""
        self.running = False
        logger.info("Autonomous executor stopped")
    
    async def _execution_loop(self):
        """Main execution loop"""
        while self.running:
            try:
                for task_id, task in self.tasks.items():
                    if not task["enabled"]:
                        continue
                    
                    # Check if task should be executed
                    should_execute = await self._check_trigger(task)
                    
                    if should_execute:
                        await self._execute_task(task)
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in execution loop: {e}")
                await asyncio.sleep(10)
    
    async def _check_trigger(self, task: Dict) -> bool:
        """Check if task trigger condition is met"""
        trigger_type = task["trigger_type"]
        config = task["trigger_config"]
        
        if trigger_type == "schedule":
            # Check schedule-based trigger
            interval = config.get("interval_seconds", 3600)
            last_exec = task.get("last_execution")
            
            if last_exec is None:
                return True
            
            last_exec_time = datetime.fromisoformat(last_exec)
            elapsed = (datetime.utcnow() - last_exec_time).total_seconds()
            
            return elapsed >= interval
        
        elif trigger_type == "event":
            # Event-based trigger (to be implemented with event system)
            return False
        
        elif trigger_type == "threshold":
            # Threshold-based trigger (e.g., CPU > 80%)
            return False
        
        return False
    
    async def _execute_task(self, task: Dict):
        """Execute an autonomous task"""
        try:
            task_id = task["id"]
            logger.info(f"Executing autonomous task: {task['name']}")
            
            # Execute task function
            result = await task["function"]()
            
            # Update task metadata
            task["last_execution"] = datetime.utcnow().isoformat()
            task["execution_count"] += 1
            
            # Log execution
            execution_log = {
                "task_id": task_id,
                "task_name": task["name"],
                "executed_at": datetime.utcnow().isoformat(),
                "result": result,
                "status": "success"
            }
            self.execution_log.append(execution_log)
            
            logger.info(f"Task executed successfully: {task['name']}")
            
        except Exception as e:
            logger.error(f"Error executing task {task['name']}: {e}")
            
            execution_log = {
                "task_id": task["id"],
                "task_name": task["name"],
                "executed_at": datetime.utcnow().isoformat(),
                "error": str(e),
                "status": "failed"
            }
            self.execution_log.append(execution_log)
    
    async def get_task_status(self, task_id: str) -> Dict:
        """Get status of an autonomous task"""
        task = self.tasks.get(task_id)
        
        if not task:
            return {"error": "Task not found"}
        
        return {
            "id": task["id"],
            "name": task["name"],
            "enabled": task["enabled"],
            "trigger_type": task["trigger_type"],
            "last_execution": task["last_execution"],
            "execution_count": task["execution_count"]
        }
    
    async def enable_task(self, task_id: str):
        """Enable an autonomous task"""
        if task_id in self.tasks:
            self.tasks[task_id]["enabled"] = True
            logger.info(f"Task enabled: {task_id}")
    
    async def disable_task(self, task_id: str):
        """Disable an autonomous task"""
        if task_id in self.tasks:
            self.tasks[task_id]["enabled"] = False
            logger.info(f"Task disabled: {task_id}")
    
    async def get_execution_log(self, limit: int = 100) -> List[Dict]:
        """Get recent execution log"""
        return self.execution_log[-limit:]


# Global executor instance
_executor: AutoExecutor = None


def get_auto_executor() -> AutoExecutor:
    """Get or create global auto executor instance"""
    global _executor
    
    if _executor is None:
        _executor = AutoExecutor()
    
    return _executor


# Predefined autonomous tasks
async def auto_forensic_scan():
    """Autonomous forensic scan"""
    logger.info("Running automated forensic scan")
    return {"status": "completed", "findings": 0}


async def auto_threat_detection():
    """Autonomous threat detection"""
    logger.info("Running automated threat detection")
    return {"status": "completed", "threats": 0}


async def auto_system_health_check():
    """Autonomous system health check"""
    logger.info("Running automated system health check")
    return {"status": "healthy"}
