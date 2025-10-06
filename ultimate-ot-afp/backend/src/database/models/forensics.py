"""
Forensics Database Models
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ...core.database import Base


class ForensicCase(Base):
    """Forensic Case model"""
    __tablename__ = "forensic_cases"
    
    id = Column(String, primary_key=True)
    case_number = Column(String, unique=True, index=True)
    case_name = Column(String)
    description = Column(Text)
    
    # Case details
    investigator = Column(String)
    status = Column(String, default="open")  # open, in_progress, closed
    priority = Column(String, default="medium")  # low, medium, high, critical
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    # Metadata
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})
    
    # Relationships
    evidence = relationship("Evidence", back_populates="case", cascade="all, delete-orphan")
    timeline = relationship("Timeline", back_populates="case", cascade="all, delete-orphan")


class Evidence(Base):
    """Evidence model"""
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True)
    case_id = Column(String, ForeignKey("forensic_cases.id"), index=True)
    
    # Evidence details
    evidence_number = Column(String)
    evidence_type = Column(String)  # disk_image, memory_dump, file, network_capture, etc.
    description = Column(Text)
    source = Column(String)
    
    # File information
    file_path = Column(String)
    file_size = Column(BigInteger)
    file_hash_md5 = Column(String)
    file_hash_sha1 = Column(String)
    file_hash_sha256 = Column(String)
    
    # Chain of custody
    collected_by = Column(String)
    collected_at = Column(DateTime)
    verified = Column(Boolean, default=False)
    
    # Analysis
    analyzed = Column(Boolean, default=False)
    analysis_results = Column(JSON, default={})
    
    # Metadata
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])
    
    # Relationships
    case = relationship("ForensicCase", back_populates="evidence")


class Timeline(Base):
    """Timeline event model"""
    __tablename__ = "timeline_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, ForeignKey("forensic_cases.id"), index=True)
    
    # Event details
    timestamp = Column(DateTime, index=True)
    event_type = Column(String)
    source = Column(String)
    description = Column(Text)
    
    # Analysis
    severity = Column(String, default="info")  # info, low, medium, high, critical
    confidence = Column(Integer, default=100)  # 0-100
    
    # Metadata
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])
    
    # Relationships
    case = relationship("ForensicCase", back_populates="timeline")
