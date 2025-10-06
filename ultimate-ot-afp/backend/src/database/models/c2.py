"""
C2 (Command & Control) Database Models
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ...core.database import Base


class Implant(Base):
    """C2 Implant model"""
    __tablename__ = "implants"
    
    id = Column(String, primary_key=True)
    hostname = Column(String, index=True)
    ip_address = Column(String)
    operating_system = Column(String)
    username = Column(String)
    privileges = Column(String)
    implant_version = Column(String)
    api_key = Column(String, unique=True, index=True)
    
    # Status
    status = Column(String, default="active")  # active, inactive, compromised
    last_seen = Column(DateTime, default=datetime.utcnow)
    first_seen = Column(DateTime, default=datetime.utcnow)
    
    # Metadata
    metadata = Column(JSON, default={})
    
    # Relationships
    tasks = relationship("Task", back_populates="implant", cascade="all, delete-orphan")
    communications = relationship("C2Communication", back_populates="implant", cascade="all, delete-orphan")


class Task(Base):
    """C2 Task model"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    implant_id = Column(String, ForeignKey("implants.id"), index=True)
    
    # Task details
    task_type = Column(String)  # shell, download, upload, persistence, etc.
    command = Column(Text)
    parameters = Column(JSON, default={})
    
    # Status
    status = Column(String, default="pending")  # pending, executing, completed, failed
    priority = Column(Integer, default=5)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Results
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    
    # Relationships
    implant = relationship("Implant", back_populates="tasks")


class C2Communication(Base):
    """C2 Communication log"""
    __tablename__ = "c2_communications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    implant_id = Column(String, ForeignKey("implants.id"), index=True)
    
    # Communication details
    direction = Column(String)  # inbound, outbound
    message_type = Column(String)  # heartbeat, task_request, task_response, etc.
    payload = Column(JSON)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    size_bytes = Column(Integer)
    encrypted = Column(Boolean, default=True)
    
    # Relationships
    implant = relationship("Implant", back_populates="communications")
