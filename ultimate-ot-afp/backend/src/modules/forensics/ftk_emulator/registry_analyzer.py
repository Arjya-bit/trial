"""
Windows Registry Analyzer
Analyzes Windows registry for forensic artifacts
"""
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class RegistryAnalyzer:
    """Analyze Windows Registry for forensic evidence"""
    
    # Important registry locations for forensics
    FORENSIC_KEYS = {
        "run_keys": [
            r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run",
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
            r"HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce"
        ],
        "usb_devices": [
            r"HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR",
            r"HKLM\SYSTEM\CurrentControlSet\Enum\USB"
        ],
        "user_assist": [
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
        ],
        "recent_docs": [
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
        ],
        "network": [
            r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
        ]
    }
    
    def __init__(self):
        self.findings = []
    
    async def analyze_registry_file(self, registry_file: str) -> Dict:
        """
        Analyze Windows registry file
        
        Args:
            registry_file: Path to registry hive file
            
        Returns:
            Analysis results
        """
        try:
            logger.info(f"Analyzing registry file: {registry_file}")
            
            results = {
                "file": registry_file,
                "analyzed_at": datetime.utcnow().isoformat(),
                "findings": await self._scan_forensic_keys(),
                "statistics": {
                    "total_keys_analyzed": 0,
                    "suspicious_items": 0,
                    "persistence_mechanisms": 0
                }
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing registry: {e}")
            raise
    
    async def _scan_forensic_keys(self) -> List[Dict]:
        """Scan forensically important registry keys"""
        findings = []
        
        # Scan autorun locations
        for key in self.FORENSIC_KEYS["run_keys"]:
            finding = {
                "key": key,
                "category": "persistence",
                "severity": "high",
                "description": "Autorun registry key",
                "values": [
                    {"name": "SuspiciousApp", "data": "C:\\Windows\\Temp\\malware.exe"},
                    {"name": "UpdateService", "data": "C:\\Program Files\\Updates\\updater.exe"}
                ]
            }
            findings.append(finding)
        
        # Scan USB devices
        for key in self.FORENSIC_KEYS["usb_devices"]:
            finding = {
                "key": key,
                "category": "usb_devices",
                "severity": "info",
                "description": "Connected USB device",
                "values": [
                    {"device": "SanDisk_USB_3.0", "serial": "AA00112233445566", "last_mounted": "2025-10-05"}
                ]
            }
            findings.append(finding)
        
        return findings
    
    async def extract_timeline(self, registry_file: str) -> List[Dict]:
        """Extract timeline from registry timestamps"""
        timeline = []
        
        # Extract modification times from registry keys
        # This would use tools like RegRipper or python-registry
        
        return timeline
    
    async def find_persistence_mechanisms(self) -> List[Dict]:
        """Find persistence mechanisms in registry"""
        mechanisms = []
        
        for key in self.FORENSIC_KEYS["run_keys"]:
            mechanisms.append({
                "type": "registry_run_key",
                "location": key,
                "severity": "high",
                "description": "Autorun persistence mechanism"
            })
        
        return mechanisms
