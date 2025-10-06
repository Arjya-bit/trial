"""
Process Monitor
Real-time process monitoring and analysis
"""
import psutil
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ProcessMonitor:
    """Monitor and analyze system processes"""
    
    def __init__(self):
        self.suspicious_processes = []
        self.whitelist = set()
    
    async def get_all_processes(self) -> List[Dict]:
        """Get list of all running processes"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    proc_data = {
                        "pid": info['pid'],
                        "name": info['name'],
                        "username": info.get('username', 'N/A'),
                        "status": info['status'],
                        "cpu_percent": info.get('cpu_percent', 0),
                        "memory_percent": info.get('memory_percent', 0),
                        "num_threads": proc.num_threads(),
                        "create_time": datetime.fromtimestamp(proc.create_time()).isoformat(),
                        "cmdline": ' '.join(proc.cmdline()) if proc.cmdline() else '',
                    }
                    processes.append(proc_data)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return processes
            
        except Exception as e:
            logger.error(f"Error getting processes: {e}")
            raise
    
    async def get_process_details(self, pid: int) -> Optional[Dict]:
        """Get detailed information about a specific process"""
        try:
            proc = psutil.Process(pid)
            
            details = {
                "pid": proc.pid,
                "name": proc.name(),
                "exe": proc.exe(),
                "cwd": proc.cwd(),
                "cmdline": proc.cmdline(),
                "username": proc.username(),
                "status": proc.status(),
                "create_time": datetime.fromtimestamp(proc.create_time()).isoformat(),
                "cpu_percent": proc.cpu_percent(interval=0.1),
                "memory_info": {
                    "rss": proc.memory_info().rss,
                    "vms": proc.memory_info().vms,
                    "percent": proc.memory_percent()
                },
                "num_threads": proc.num_threads(),
                "num_fds": proc.num_fds() if hasattr(proc, 'num_fds') else 0,
                "connections": await self._get_process_connections(proc),
                "open_files": await self._get_open_files(proc)
            }
            
            return details
            
        except psutil.NoSuchProcess:
            return None
        except Exception as e:
            logger.error(f"Error getting process details: {e}")
            raise
    
    async def _get_process_connections(self, proc: psutil.Process) -> List[Dict]:
        """Get network connections for a process"""
        try:
            connections = []
            for conn in proc.connections():
                connections.append({
                    "fd": conn.fd,
                    "family": str(conn.family),
                    "type": str(conn.type),
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    "status": conn.status
                })
            return connections
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return []
    
    async def _get_open_files(self, proc: psutil.Process) -> List[str]:
        """Get open files for a process"""
        try:
            return [f.path for f in proc.open_files()]
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return []
    
    async def kill_process(self, pid: int, force: bool = False) -> bool:
        """Kill a process"""
        try:
            proc = psutil.Process(pid)
            
            if force:
                proc.kill()
            else:
                proc.terminate()
            
            logger.info(f"Process terminated: PID {pid}")
            return True
            
        except psutil.NoSuchProcess:
            return False
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            raise
    
    async def analyze_suspicious_processes(self) -> List[Dict]:
        """Analyze and identify suspicious processes"""
        try:
            suspicious = []
            
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'connections']):
                try:
                    info = proc.info
                    
                    # Check for suspicious indicators
                    is_suspicious = False
                    reasons = []
                    
                    # Check for processes without executable path
                    if not info.get('exe'):
                        is_suspicious = True
                        reasons.append("No executable path")
                    
                    # Check for high CPU usage
                    cpu = proc.cpu_percent(interval=0.1)
                    if cpu > 80:
                        is_suspicious = True
                        reasons.append(f"High CPU usage: {cpu}%")
                    
                    # Check for suspicious names
                    suspicious_keywords = ['keylog', 'inject', 'exploit', 'backdoor', 'rootkit']
                    if any(keyword in info['name'].lower() for keyword in suspicious_keywords):
                        is_suspicious = True
                        reasons.append("Suspicious process name")
                    
                    if is_suspicious:
                        suspicious.append({
                            "pid": info['pid'],
                            "name": info['name'],
                            "exe": info.get('exe', 'N/A'),
                            "reasons": reasons,
                            "severity": "high" if len(reasons) > 1 else "medium"
                        })
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.suspicious_processes = suspicious
            return suspicious
            
        except Exception as e:
            logger.error(f"Error analyzing suspicious processes: {e}")
            raise
    
    async def get_system_stats(self) -> Dict:
        """Get overall system statistics"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "cpu_count": psutil.cpu_count(),
                "memory": {
                    "total": psutil.virtual_memory().total,
                    "available": psutil.virtual_memory().available,
                    "percent": psutil.virtual_memory().percent,
                    "used": psutil.virtual_memory().used
                },
                "disk": {
                    "total": psutil.disk_usage('/').total,
                    "used": psutil.disk_usage('/').used,
                    "free": psutil.disk_usage('/').free,
                    "percent": psutil.disk_usage('/').percent
                },
                "process_count": len(psutil.pids()),
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            raise
