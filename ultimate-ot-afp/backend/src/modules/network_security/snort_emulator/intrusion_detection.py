"""
Snort-style Intrusion Detection System
Real-time network intrusion detection
"""
import logging
from typing import Dict, List
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class IntrusionDetectionSystem:
    """Network Intrusion Detection System"""
    
    def __init__(self):
        self.rules = []
        self.alerts = []
        self.load_default_rules()
    
    def load_default_rules(self):
        """Load default detection rules"""
        self.rules = [
            {
                "id": "1001",
                "name": "SQL Injection Attempt",
                "pattern": r"(union.*select|select.*from|insert.*into)",
                "severity": "high",
                "category": "web_attack"
            },
            {
                "id": "1002",
                "name": "Port Scan Detected",
                "pattern": "port_scan",
                "severity": "medium",
                "category": "reconnaissance"
            },
            {
                "id": "1003",
                "name": "Brute Force Attack",
                "pattern": "failed_login",
                "severity": "high",
                "category": "authentication"
            },
            {
                "id": "1004",
                "name": "Suspicious Outbound Connection",
                "pattern": r"(known_bad_ip|suspicious_port)",
                "severity": "high",
                "category": "malware"
            },
            {
                "id": "1005",
                "name": "DDoS Attack Pattern",
                "pattern": "high_packet_rate",
                "severity": "critical",
                "category": "dos"
            }
        ]
    
    async def analyze_packet(self, packet_data: Dict) -> Dict:
        """
        Analyze network packet for threats
        
        Args:
            packet_data: Packet information
            
        Returns:
            Analysis result with alerts
        """
        try:
            alerts_triggered = []
            
            payload = packet_data.get("payload", "")
            src_ip = packet_data.get("source_ip")
            dst_ip = packet_data.get("destination_ip")
            protocol = packet_data.get("protocol")
            
            # Check against rules
            for rule in self.rules:
                if self._check_rule(rule, packet_data, payload):
                    alert = {
                        "alert_id": f"ALERT-{datetime.utcnow().timestamp()}",
                        "rule_id": rule["id"],
                        "rule_name": rule["name"],
                        "severity": rule["severity"],
                        "category": rule["category"],
                        "source_ip": src_ip,
                        "destination_ip": dst_ip,
                        "protocol": protocol,
                        "timestamp": datetime.utcnow().isoformat(),
                        "description": f"{rule['name']} detected from {src_ip} to {dst_ip}"
                    }
                    alerts_triggered.append(alert)
                    self.alerts.append(alert)
                    logger.warning(f"IDS Alert: {rule['name']} - {src_ip} -> {dst_ip}")
            
            return {
                "packet_id": packet_data.get("id"),
                "analyzed_at": datetime.utcnow().isoformat(),
                "alerts": alerts_triggered,
                "threat_detected": len(alerts_triggered) > 0,
                "severity": max([a["severity"] for a in alerts_triggered], default="none")
            }
            
        except Exception as e:
            logger.error(f"Error analyzing packet: {e}")
            raise
    
    def _check_rule(self, rule: Dict, packet_data: Dict, payload: str) -> bool:
        """Check if packet matches a rule"""
        try:
            pattern = rule["pattern"]
            
            # Check payload against pattern
            if re.search(pattern, payload, re.IGNORECASE):
                return True
            
            # Additional checks based on category
            if rule["category"] == "reconnaissance":
                # Check for port scanning behavior
                if packet_data.get("destination_port", 0) > 1024:
                    return False
            
            return False
            
        except Exception:
            return False
    
    async def get_alerts(
        self,
        severity: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get recent alerts"""
        alerts = self.alerts
        
        if severity:
            alerts = [a for a in alerts if a["severity"] == severity]
        
        return alerts[-limit:]
    
    async def get_statistics(self) -> Dict:
        """Get IDS statistics"""
        total_alerts = len(self.alerts)
        
        severity_counts = {
            "critical": len([a for a in self.alerts if a["severity"] == "critical"]),
            "high": len([a for a in self.alerts if a["severity"] == "high"]),
            "medium": len([a for a in self.alerts if a["severity"] == "medium"]),
            "low": len([a for a in self.alerts if a["severity"] == "low"])
        }
        
        category_counts = {}
        for alert in self.alerts:
            category = alert["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "total_alerts": total_alerts,
            "severity_distribution": severity_counts,
            "category_distribution": category_counts,
            "active_rules": len(self.rules)
        }
    
    async def add_custom_rule(self, rule: Dict) -> str:
        """Add a custom detection rule"""
        rule_id = f"CUSTOM-{len(self.rules) + 1000}"
        rule["id"] = rule_id
        self.rules.append(rule)
        logger.info(f"Custom rule added: {rule_id}")
        return rule_id


# Global IDS instance
_ids_instance = None


def get_ids() -> IntrusionDetectionSystem:
    """Get or create global IDS instance"""
    global _ids_instance
    
    if _ids_instance is None:
        _ids_instance = IntrusionDetectionSystem()
    
    return _ids_instance
