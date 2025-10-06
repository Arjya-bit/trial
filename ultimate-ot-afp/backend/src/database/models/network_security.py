"""
Network Security Database Models
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text, BigInteger, Boolean, Float
from datetime import datetime
from ...core.database import Base


class NetworkCapture(Base):
    """Network capture/packet model"""
    __tablename__ = "network_captures"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Capture details
    session_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Network information
    source_ip = Column(String, index=True)
    source_port = Column(Integer)
    destination_ip = Column(String, index=True)
    destination_port = Column(Integer)
    protocol = Column(String, index=True)
    
    # Packet data
    packet_size = Column(Integer)
    payload = Column(Text)
    headers = Column(JSON)
    
    # Analysis
    analyzed = Column(Boolean, default=False)
    malicious = Column(Boolean, default=False)
    severity = Column(String, default="info")
    
    # Metadata
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])


class Alert(Base):
    """Security alert model"""
    __tablename__ = "security_alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Alert details
    alert_type = Column(String, index=True)  # ids, vulnerability, anomaly, etc.
    severity = Column(String, index=True)  # info, low, medium, high, critical
    title = Column(String)
    description = Column(Text)
    
    # Source
    source = Column(String)  # snort, wireshark, custom, etc.
    source_ip = Column(String)
    destination_ip = Column(String)
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    occurrence_count = Column(Integer, default=1)
    
    # Status
    status = Column(String, default="new")  # new, investigating, resolved, false_positive
    assigned_to = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Details
    details = Column(JSON, default={})
    remediation = Column(Text, nullable=True)
    
    # Metadata
    tags = Column(JSON, default=[])


class Vulnerability(Base):
    """Vulnerability model"""
    __tablename__ = "vulnerabilities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Vulnerability details
    cve_id = Column(String, unique=True, index=True, nullable=True)
    title = Column(String)
    description = Column(Text)
    severity = Column(String, index=True)  # low, medium, high, critical
    cvss_score = Column(Float, nullable=True)
    
    # Target
    target_type = Column(String)  # host, application, network, ot_device
    target_identifier = Column(String)
    affected_component = Column(String)
    
    # Discovery
    discovered_by = Column(String)  # scanner_name or manual
    discovered_at = Column(DateTime, default=datetime.utcnow)
    
    # Status
    status = Column(String, default="open")  # open, mitigated, patched, accepted_risk
    verified = Column(Boolean, default=False)
    
    # Remediation
    remediation = Column(Text, nullable=True)
    patch_available = Column(Boolean, default=False)
    patch_details = Column(Text, nullable=True)
    
    # Metadata
    references = Column(JSON, default=[])
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})
