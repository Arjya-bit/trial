"""
Service Installer
Installs application as a system service for persistence
"""
import os
import sys
import platform
import subprocess
import logging

logger = logging.getLogger(__name__)


class ServiceInstaller:
    """Install as system service"""
    
    def __init__(self, service_name: str = "OT-AFP-Service"):
        self.service_name = service_name
        self.platform = platform.system()
    
    def install(self, executable_path: str) -> bool:
        """Install service"""
        logger.info(f"Installing service on {self.platform}")
        
        if self.platform == "Windows":
            return self._install_windows(executable_path)
        elif self.platform == "Linux":
            return self._install_linux(executable_path)
        else:
            logger.warning(f"Unsupported platform: {self.platform}")
            return False
    
    def _install_windows(self, executable_path: str) -> bool:
        """Install Windows service"""
        try:
            # Using sc.exe to create service
            cmd = [
                "sc.exe", "create", self.service_name,
                f"binPath= {executable_path}",
                "start= auto"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Windows service installed successfully")
                return True
            else:
                logger.error(f"Service installation failed: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error installing Windows service: {e}")
            return False
    
    def _install_linux(self, executable_path: str) -> bool:
        """Install Linux systemd service"""
        try:
            service_content = f"""[Unit]
Description=Ultimate OT-AFP Platform
After=network.target

[Service]
Type=simple
ExecStart={executable_path}
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""
            
            service_file = f"/etc/systemd/system/{self.service_name}.service"
            
            with open(service_file, 'w') as f:
                f.write(service_content)
            
            # Enable and start service
            subprocess.run(["systemctl", "daemon-reload"])
            subprocess.run(["systemctl", "enable", self.service_name])
            subprocess.run(["systemctl", "start", self.service_name])
            
            logger.info("Linux systemd service installed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error installing Linux service: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Uninstall service"""
        if self.platform == "Windows":
            subprocess.run(["sc.exe", "delete", self.service_name])
        elif self.platform == "Linux":
            subprocess.run(["systemctl", "stop", self.service_name])
            subprocess.run(["systemctl", "disable", self.service_name])
            os.remove(f"/etc/systemd/system/{self.service_name}.service")
        
        return True
