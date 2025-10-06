"""
Admin Privilege Escalator
Attempts to gain administrative privileges
"""
import os
import sys
import platform
import subprocess
import logging

logger = logging.getLogger(__name__)


class AdminEscalator:
    """Escalate privileges to administrator/root"""
    
    def __init__(self):
        self.platform = platform.system()
    
    def is_admin(self) -> bool:
        """Check if running with admin privileges"""
        try:
            if self.platform == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except Exception:
            return False
    
    def escalate(self):
        """Attempt privilege escalation"""
        if self.is_admin():
            logger.info("Already running with admin privileges")
            return True
        
        logger.info(f"Attempting privilege escalation on {self.platform}")
        
        if self.platform == "Windows":
            return self._escalate_windows()
        elif self.platform == "Linux":
            return self._escalate_linux()
        else:
            logger.warning(f"Unsupported platform: {self.platform}")
            return False
    
    def _escalate_windows(self) -> bool:
        """Windows privilege escalation"""
        try:
            import ctypes
            
            # Request UAC elevation
            if not self.is_admin():
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                return True
        except Exception as e:
            logger.error(f"Windows escalation failed: {e}")
        
        return False
    
    def _escalate_linux(self) -> bool:
        """Linux privilege escalation"""
        try:
            # Try sudo
            result = subprocess.run(
                ['sudo', '-n', 'true'],
                capture_output=True,
                timeout=1
            )
            
            if result.returncode == 0:
                logger.info("Sudo access available")
                return True
        except Exception as e:
            logger.error(f"Linux escalation failed: {e}")
        
        return False


if __name__ == "__main__":
    escalator = AdminEscalator()
    print(f"Running as admin: {escalator.is_admin()}")
    
    if not escalator.is_admin():
        escalator.escalate()
