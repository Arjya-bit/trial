"""
Autonomous Execution Engine for Ultimate OT-AFP Platform
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from pathlib import Path
import time
import json
import schedule
from enum import Enum

from ...core.config import settings
from ..stealth.stealth_operations import StealthManager
from ..persistence.persistence_manager import PersistenceManager
from ..forensics.autopsy_emulator.hash_analysis import autopsy_emulator
from ..ai_model.model_inference import inference_engine

logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class AutonomousTask:
    """Autonomous task definition"""
    task_id: str
    name: str
    description: str
    priority: TaskPriority
    trigger_conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    cooldown_seconds: int = 300
    max_retries: int = 3
    enabled: bool = True
    last_execution: Optional[float] = None
    execution_count: int = 0
    failure_count: int = 0

@dataclass
class ExecutionResult:
    """Result of autonomous task execution"""
    task_id: str
    success: bool
    execution_time: float
    output: Any
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = None

class AutonomousExecutor:
    """Advanced Autonomous Execution Engine"""
    
    def __init__(self):
        self.tasks = {}
        self.running = False
        self.execution_history = []
        self.stealth_manager = None
        self.persistence_manager = None
        self.task_queue = asyncio.Queue()
        self.workers = []
        self.metrics = {
            "tasks_executed": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "avg_execution_time": 0.0
        }
        logger.info("🤖 Autonomous Executor initialized")
    
    async def start(self):
        """Start the autonomous execution engine"""
        try:
            if self.running:
                logger.warning("⚠️ Autonomous executor already running")
                return
            
            self.running = True
            
            # Initialize dependencies
            from ..stealth.stealth_operations import stealth_manager
            from ..persistence.persistence_manager import persistence_manager
            
            self.stealth_manager = stealth_manager
            self.persistence_manager = persistence_manager
            
            # Load default tasks
            await self._load_default_tasks()
            
            # Start worker threads
            for i in range(settings.MAX_WORKERS):
                worker = asyncio.create_task(self._task_worker(f"worker_{i}"))
                self.workers.append(worker)
            
            # Start monitoring loop
            asyncio.create_task(self._monitoring_loop())
            
            # Start scheduled task checker
            asyncio.create_task(self._scheduled_task_checker())
            
            logger.info("🚀 Autonomous Executor started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start Autonomous Executor: {e}")
            self.running = False
            raise
    
    async def stop(self):
        """Stop the autonomous execution engine"""
        try:
            self.running = False
            
            # Cancel all workers
            for worker in self.workers:
                worker.cancel()
            
            # Wait for workers to finish
            await asyncio.gather(*self.workers, return_exceptions=True)
            
            logger.info("🛑 Autonomous Executor stopped")
            
        except Exception as e:
            logger.error(f"❌ Error stopping Autonomous Executor: {e}")
    
    async def register_task(self, task: AutonomousTask):
        """Register a new autonomous task"""
        try:
            self.tasks[task.task_id] = task
            logger.info(f"📝 Registered autonomous task: {task.name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to register task: {e}")
    
    async def execute_task(self, task_id: str, force: bool = False) -> ExecutionResult:
        """Execute a specific autonomous task"""
        try:
            if task_id not in self.tasks:
                raise ValueError(f"Task {task_id} not found")
            
            task = self.tasks[task_id]
            
            if not task.enabled and not force:
                return ExecutionResult(
                    task_id=task_id,
                    success=False,
                    execution_time=0.0,
                    output=None,
                    error_message="Task is disabled"
                )
            
            # Check cooldown
            if not force and task.last_execution:
                time_since_last = time.time() - task.last_execution
                if time_since_last < task.cooldown_seconds:
                    return ExecutionResult(
                        task_id=task_id,
                        success=False,
                        execution_time=0.0,
                        output=None,
                        error_message=f"Task in cooldown ({time_since_last:.1f}s remaining)"
                    )
            
            logger.info(f"🔄 Executing autonomous task: {task.name}")
            start_time = time.time()
            
            try:
                # Execute task actions
                results = []
                for action in task.actions:
                    result = await self._execute_action(action)
                    results.append(result)
                
                execution_time = time.time() - start_time
                
                # Update task metadata
                task.last_execution = time.time()
                task.execution_count += 1
                
                # Update metrics
                self.metrics["tasks_executed"] += 1
                self.metrics["successful_executions"] += 1
                self._update_avg_execution_time(execution_time)
                
                execution_result = ExecutionResult(
                    task_id=task_id,
                    success=True,
                    execution_time=execution_time,
                    output=results,
                    metrics={
                        "actions_executed": len(results),
                        "task_priority": task.priority.name
                    }
                )
                
                self.execution_history.append(execution_result)
                logger.info(f"✅ Task executed successfully: {task.name} ({execution_time:.2f}s)")
                
                return execution_result
                
            except Exception as e:
                execution_time = time.time() - start_time
                task.failure_count += 1
                
                # Update metrics
                self.metrics["tasks_executed"] += 1
                self.metrics["failed_executions"] += 1
                
                execution_result = ExecutionResult(
                    task_id=task_id,
                    success=False,
                    execution_time=execution_time,
                    output=None,
                    error_message=str(e)
                )
                
                self.execution_history.append(execution_result)
                logger.error(f"❌ Task execution failed: {task.name} - {e}")
                
                return execution_result
                
        except Exception as e:
            logger.error(f"❌ Critical error executing task {task_id}: {e}")
            return ExecutionResult(
                task_id=task_id,
                success=False,
                execution_time=0.0,
                output=None,
                error_message=f"Critical error: {e}"
            )
    
    async def _execute_action(self, action: Dict[str, Any]) -> Any:
        """Execute a single action"""
        action_type = action.get("type")
        
        if action_type == "forensic_scan":
            return await self._execute_forensic_scan(action)
        elif action_type == "stealth_operation":
            return await self._execute_stealth_operation(action)
        elif action_type == "persistence_check":
            return await self._execute_persistence_check(action)
        elif action_type == "ai_analysis":
            return await self._execute_ai_analysis(action)
        elif action_type == "network_scan":
            return await self._execute_network_scan(action)
        elif action_type == "system_cleanup":
            return await self._execute_system_cleanup(action)
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    
    async def _execute_forensic_scan(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute forensic scanning action"""
        scan_type = action.get("scan_type", "hash_analysis")
        target_path = action.get("target_path", "./")
        
        if scan_type == "hash_analysis":
            # Perform hash analysis on target files
            results = []
            target = Path(target_path)
            
            if target.is_file():
                files_to_scan = [target]
            else:
                files_to_scan = list(target.glob("**/*"))[:100]  # Limit to 100 files
            
            for file_path in files_to_scan:
                if file_path.is_file():
                    try:
                        hash_result = await autopsy_emulator.hash_analysis(str(file_path))
                        if hash_result.known_bad or hash_result.reputation_score < 0.3:
                            results.append({
                                "file": str(file_path),
                                "suspicious": True,
                                "reason": "Known bad hash" if hash_result.known_bad else "Low reputation",
                                "hash": hash_result.sha256
                            })
                    except Exception:
                        continue
            
            return {"scan_type": scan_type, "suspicious_files": results}
        
        return {"scan_type": scan_type, "status": "completed"}
    
    async def _execute_stealth_operation(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute stealth operation action"""
        if not self.stealth_manager:
            return {"status": "error", "message": "Stealth manager not available"}
        
        operation = action.get("operation", "check_status")
        
        if operation == "hide_process":
            process_name = action.get("process_name", "python")
            result = await self.stealth_manager.hide_process(process_name)
            return {"operation": operation, "success": result}
        
        elif operation == "check_detection":
            detection_result = await self.stealth_manager.check_av_detection()
            return {"operation": operation, "detected": detection_result}
        
        return {"operation": operation, "status": "completed"}
    
    async def _execute_persistence_check(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute persistence checking action"""
        if not self.persistence_manager:
            return {"status": "error", "message": "Persistence manager not available"}
        
        check_type = action.get("check_type", "verify_all")
        
        if check_type == "verify_all":
            status = await self.persistence_manager.check_persistence_status()
            return {"check_type": check_type, "status": status}
        
        return {"check_type": check_type, "status": "completed"}
    
    async def _execute_ai_analysis(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI analysis action"""
        analysis_type = action.get("analysis_type", "general")
        data = action.get("data")
        
        if analysis_type == "malware_detection" and data:
            result = await inference_engine.predict("malware-detection-model", data)
            return {"analysis_type": analysis_type, "prediction": result.prediction, "confidence": result.confidence}
        
        return {"analysis_type": analysis_type, "status": "completed"}
    
    async def _execute_network_scan(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute network scanning action"""
        scan_type = action.get("scan_type", "port_scan")
        target = action.get("target", "127.0.0.1")
        
        # Simulate network scan
        return {"scan_type": scan_type, "target": target, "status": "completed", "results": []}
    
    async def _execute_system_cleanup(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system cleanup action"""
        cleanup_type = action.get("cleanup_type", "logs")
        
        # Simulate cleanup
        return {"cleanup_type": cleanup_type, "status": "completed", "files_cleaned": 0}
    
    async def _task_worker(self, worker_name: str):
        """Worker thread for processing autonomous tasks"""
        logger.info(f"👷 Starting task worker: {worker_name}")
        
        while self.running:
            try:
                # Get task from queue with timeout
                task_id = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Execute the task
                result = await self.execute_task(task_id)
                
                # Mark task as done
                self.task_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"❌ Worker {worker_name} error: {e}")
        
        logger.info(f"🛑 Task worker stopped: {worker_name}")
    
    async def _monitoring_loop(self):
        """Continuous monitoring loop"""
        while self.running:
            try:
                # Check system conditions and trigger tasks
                await self._check_trigger_conditions()
                
                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Monitoring loop error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _scheduled_task_checker(self):
        """Check for scheduled tasks"""
        while self.running:
            try:
                schedule.run_pending()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"❌ Scheduled task checker error: {e}")
    
    async def _check_trigger_conditions(self):
        """Check trigger conditions for all tasks"""
        for task_id, task in self.tasks.items():
            if not task.enabled:
                continue
            
            try:
                # Check if trigger conditions are met
                should_execute = await self._evaluate_trigger_conditions(task.trigger_conditions)
                
                if should_execute:
                    await self.task_queue.put(task_id)
                    
            except Exception as e:
                logger.error(f"❌ Error checking trigger conditions for {task_id}: {e}")
    
    async def _evaluate_trigger_conditions(self, conditions: Dict[str, Any]) -> bool:
        """Evaluate trigger conditions"""
        try:
            condition_type = conditions.get("type", "time_based")
            
            if condition_type == "time_based":
                interval = conditions.get("interval_seconds", 3600)
                last_run = conditions.get("last_run", 0)
                return (time.time() - last_run) >= interval
            
            elif condition_type == "event_based":
                # Check for specific system events
                return False  # Placeholder
            
            elif condition_type == "threshold_based":
                # Check system metrics against thresholds
                return False  # Placeholder
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error evaluating trigger conditions: {e}")
            return False
    
    async def _load_default_tasks(self):
        """Load default autonomous tasks"""
        try:
            default_tasks = [
                AutonomousTask(
                    task_id="auto_forensic_scan",
                    name="Automated Forensic Scan",
                    description="Automatically scan for suspicious files",
                    priority=TaskPriority.MEDIUM,
                    trigger_conditions={"type": "time_based", "interval_seconds": 3600},
                    actions=[{
                        "type": "forensic_scan",
                        "scan_type": "hash_analysis",
                        "target_path": settings.EVIDENCE_PATH
                    }],
                    cooldown_seconds=1800
                ),
                AutonomousTask(
                    task_id="stealth_check",
                    name="Stealth Status Check",
                    description="Check stealth operation status",
                    priority=TaskPriority.HIGH,
                    trigger_conditions={"type": "time_based", "interval_seconds": 600},
                    actions=[{
                        "type": "stealth_operation",
                        "operation": "check_detection"
                    }],
                    cooldown_seconds=300
                ),
                AutonomousTask(
                    task_id="persistence_maintenance",
                    name="Persistence Maintenance", 
                    description="Maintain persistence mechanisms",
                    priority=TaskPriority.HIGH,
                    trigger_conditions={"type": "time_based", "interval_seconds": 1800},
                    actions=[{
                        "type": "persistence_check",
                        "check_type": "verify_all"
                    }],
                    cooldown_seconds=900
                )
            ]
            
            for task in default_tasks:
                await self.register_task(task)
            
            logger.info(f"📚 Loaded {len(default_tasks)} default autonomous tasks")
            
        except Exception as e:
            logger.error(f"❌ Failed to load default tasks: {e}")
    
    def _update_avg_execution_time(self, execution_time: float):
        """Update average execution time metric"""
        total_executions = self.metrics["tasks_executed"]
        if total_executions == 1:
            self.metrics["avg_execution_time"] = execution_time
        else:
            current_avg = self.metrics["avg_execution_time"]
            self.metrics["avg_execution_time"] = ((current_avg * (total_executions - 1)) + execution_time) / total_executions
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return {
            "task_id": task_id,
            "name": task.name,
            "enabled": task.enabled,
            "priority": task.priority.name,
            "execution_count": task.execution_count,
            "failure_count": task.failure_count,
            "last_execution": task.last_execution,
            "cooldown_remaining": max(0, task.cooldown_seconds - (time.time() - (task.last_execution or 0)))
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get autonomous executor system metrics"""
        return {
            **self.metrics,
            "running": self.running,
            "active_tasks": len([t for t in self.tasks.values() if t.enabled]),
            "total_tasks": len(self.tasks),
            "queue_size": self.task_queue.qsize(),
            "worker_count": len(self.workers)
        }

# Global autonomous executor instance
autonomous_executor = AutonomousExecutor()