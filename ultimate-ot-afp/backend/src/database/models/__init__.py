"""
Database Models for Ultimate OT-AFP Platform
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class ForensicsCase(Base):
    """Forensics case model"""
    __tablename__ = "forensics_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, index=True)
    case_name = Column(String, index=True)
    examiner = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default="active")
    
    # Relationships
    evidence_items = relationship("EvidenceItem", back_populates="case")
    analysis_results = relationship("AnalysisResult", back_populates="case")

class EvidenceItem(Base):
    """Evidence item model"""
    __tablename__ = "evidence_items"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("forensics_cases.case_id"))
    file_path = Column(String)
    file_name = Column(String)
    file_size = Column(Integer)
    md5_hash = Column(String, index=True)
    sha1_hash = Column(String, index=True)
    sha256_hash = Column(String, index=True)
    file_type = Column(String)
    acquired_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case = relationship("ForensicsCase", back_populates="evidence_items")
    analysis_results = relationship("AnalysisResult", back_populates="evidence_item")

class AnalysisResult(Base):
    """Analysis result model"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("forensics_cases.case_id"))
    evidence_id = Column(Integer, ForeignKey("evidence_items.id"))
    analysis_type = Column(String)  # hash, keyword_search, timeline, etc.
    result_data = Column(JSON)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case = relationship("ForensicsCase", back_populates="analysis_results")
    evidence_item = relationship("EvidenceItem", back_populates="analysis_results")

class NetworkEvent(Base):
    """Network security event model"""
    __tablename__ = "network_events"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String)  # intrusion, anomaly, scan, etc.
    source_ip = Column(String, index=True)
    destination_ip = Column(String, index=True)
    source_port = Column(Integer)
    destination_port = Column(Integer)
    protocol = Column(String)
    severity = Column(String)  # low, medium, high, critical
    description = Column(Text)
    raw_data = Column(JSON)
    processed = Column(Boolean, default=False)

class OTDevice(Base):
    """OT device model"""
    __tablename__ = "ot_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    device_name = Column(String)
    device_type = Column(String)  # PLC, HMI, SCADA, etc.
    ip_address = Column(String, index=True)
    mac_address = Column(String)
    protocol = Column(String)  # Modbus, OPC-UA, DNP3, etc.
    vendor = Column(String)
    model = Column(String)
    firmware_version = Column(String)
    last_seen = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="online")
    
    # Relationships
    events = relationship("OTEvent", back_populates="device")

class OTEvent(Base):
    """OT security event model"""
    __tablename__ = "ot_events"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("ot_devices.device_id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String)
    severity = Column(String)
    description = Column(Text)
    event_data = Column(JSON)
    acknowledged = Column(Boolean, default=False)
    
    # Relationships
    device = relationship("OTDevice", back_populates="events")

class TaskExecution(Base):
    """Task execution model"""
    __tablename__ = "task_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    task_name = Column(String)
    task_type = Column(String)
    status = Column(String)  # pending, running, completed, failed
    priority = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    result = Column(JSON)
    error_message = Column(Text)
    execution_time = Column(Float)

class SystemMetrics(Base):
    """System metrics model"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    network_rx = Column(Integer)
    network_tx = Column(Integer)
    active_processes = Column(Integer)
    active_connections = Column(Integer)

class AIModel(Base):
    """AI model tracking"""
    __tablename__ = "ai_models"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, unique=True, index=True)
    model_type = Column(String)
    model_path = Column(String)
    description = Column(Text)
    version = Column(String)
    accuracy = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    usage_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

class AIPrediction(Base):
    """AI prediction results"""
    __tablename__ = "ai_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, ForeignKey("ai_models.model_name"))
    input_data_hash = Column(String, index=True)
    prediction = Column(JSON)
    confidence = Column(Float)
    inference_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class SecurityAlert(Base):
    """Security alerts model"""
    __tablename__ = "security_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, unique=True, index=True)
    alert_type = Column(String)  # malware, intrusion, anomaly, etc.
    severity = Column(String)
    source = Column(String)  # forensics, network, ot, ai, etc.
    title = Column(String)
    description = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String)
    acknowledged_at = Column(DateTime)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)

class AuditLog(Base):
    """Audit log model"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    action = Column(String)
    resource = Column(String)
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean)