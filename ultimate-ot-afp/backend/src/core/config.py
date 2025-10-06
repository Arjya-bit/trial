"""
Core configuration for Ultimate OT-AFP Platform
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Ultimate OT-AFP Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "sqlite:///./ultimate_ot_afp.db"
    REDIS_URL: str = "redis://localhost:6379"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    
    # AI Model Configuration
    KAGGLE_USERNAME: Optional[str] = None
    KAGGLE_KEY: Optional[str] = None
    AI_MODEL_PATH: str = "./models"
    DEFAULT_AI_MODEL: str = "microsoft/DialoGPT-medium"
    
    # C2 Configuration
    C2_PORT: int = 8443
    C2_SSL_CERT: Optional[str] = None
    C2_SSL_KEY: Optional[str] = None
    
    # Stealth Configuration
    STEALTH_MODE: bool = True
    PROCESS_HIDE_LIST: List[str] = ["ultimate-ot-afp", "python", "forensics"]
    
    # Autonomous Operations
    AUTO_EXECUTION: bool = False
    AUTO_PERSISTENCE: bool = False
    AUTO_STEALTH: bool = True
    
    # Forensics Configuration
    EVIDENCE_PATH: str = "./evidence"
    CASE_PATH: str = "./cases"
    TEMP_PATH: str = "./temp"
    
    # Network Configuration
    PCAP_INTERFACE: str = "eth0"
    PCAP_BUFFER_SIZE: int = 1024 * 1024  # 1MB
    
    # OT Security Configuration
    MODBUS_PORT: int = 502
    OPC_UA_PORT: int = 4840
    DNP3_PORT: int = 20000
    
    # Monitoring
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/ultimate_ot_afp.log"
    METRICS_ENABLED: bool = True
    
    # Performance
    MAX_WORKERS: int = 4
    CHUNK_SIZE: int = 8192
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

# Ensure required directories exist
def create_directories():
    """Create required directories if they don't exist"""
    directories = [
        settings.AI_MODEL_PATH,
        settings.EVIDENCE_PATH,
        settings.CASE_PATH,
        settings.TEMP_PATH,
        Path(settings.LOG_FILE).parent,
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

# Create directories on import
create_directories()