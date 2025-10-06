"""
Task Manager Database Models
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Float, BigInteger, Boolean
from datetime import datetime
from ...core.database import Base


class Process(Base):
    """System process model"""
    __tablename__ = "system_processes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Process details
    pid = Column(Integer, index=True)
    name = Column(String, index=True)
    exe_path = Column(String)
    command_line = Column(String)
    
    # User and security
    username = Column(String)
    user_id = Column(Integer)
    integrity_level = Column(String)
    
    # Resources
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    memory_bytes = Column(BigInteger)
    threads = Column(Integer)
    handles = Column(Integer)
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    start_time = Column(DateTime)
    
    # Status
    status = Column(String)  # running, sleeping, zombie, etc.
    priority = Column(Integer)
    
    # Analysis
    suspicious = Column(Boolean, default=False)
    whitelisted = Column(Boolean, default=False)
    
    # Metadata
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])


class SystemMetric(Base):
    """System metrics model"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # CPU metrics
    cpu_percent = Column(Float)
    cpu_count = Column(Integer)
    cpu_freq_current = Column(Float)
    
    # Memory metrics
    memory_total = Column(BigInteger)
    memory_available = Column(BigInteger)
    memory_used = Column(BigInteger)
    memory_percent = Column(Float)
    
    # Disk metrics
    disk_total = Column(BigInteger)
    disk_used = Column(BigInteger)
    disk_free = Column(BigInteger)
    disk_percent = Column(Float)
    
    # Network metrics
    bytes_sent = Column(BigInteger)
    bytes_recv = Column(BigInteger)
    packets_sent = Column(BigInteger)
    packets_recv = Column(BigInteger)
    
    # System info
    boot_time = Column(DateTime)
    uptime_seconds = Column(Integer)
    
    # Metadata
    hostname = Column(String)
    metadata = Column(JSON, default={})


class Service(Base):
    """System service model"""
    __tablename__ = "system_services"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Service details
    name = Column(String, index=True)
    display_name = Column(String)
    description = Column(String)
    
    # Status
    status = Column(String, index=True)  # running, stopped, paused, etc.
    start_type = Column(String)  # automatic, manual, disabled
    
    # Process
    pid = Column(Integer, nullable=True)
    
    # Path
    binary_path = Column(String)
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Analysis
    suspicious = Column(Boolean, default=False)
    persistence_mechanism = Column(Boolean, default=False)
    
    # Metadata
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])
