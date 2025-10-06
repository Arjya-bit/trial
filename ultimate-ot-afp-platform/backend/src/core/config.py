"""
Core configuration settings for Ultimate OT-AFP Platform
"""

import os
import secrets
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings with validation"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Ultimate OT-AFP Platform"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Comprehensive Operational Technology - Advanced Forensics Platform"

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Security Settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database Settings
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_DB: int = 0
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX_PREFIX: str = "ot-afp"

    # AI Model Settings
    KAGGLE_USERNAME: Optional[str] = None
    KAGGLE_KEY: Optional[str] = None
    MODEL_CACHE_DIR: str = "/app/models"
    ENABLE_AI_ANALYSIS: bool = True

    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = "/app/uploads"
    ALLOWED_EXTENSIONS: List[str] = [
        ".pcap", ".pcapng", ".evtx", ".dd", ".e01", ".zip", ".rar",
        ".jpg", ".png", ".pdf", ".docx", ".xlsx", ".txt", ".log"
    ]

    # Forensics Settings
    VOLATILITY_PROFILE: str = "Win10x64_19041"
    YARA_RULES_DIR: str = "/app/data/yara_rules"
    HASH_DATABASES: List[str] = [
        "/app/data/nsrl",
        "/app/data/malware_hashes"
    ]

    # Network Security Settings
    SNORT_RULES_DIR: str = "/app/data/snort_rules"
    SURICATA_RULES_DIR: str = "/app/data/suricata_rules"
    ENABLE_PACKET_CAPTURE: bool = True
    PACKET_CAPTURE_INTERFACE: str = "eth0"

    # OT Security Settings
    MODBUS_PORT: int = 502
    DNP3_PORT: int = 20000
    OPC_UA_PORT: int = 4840
    SIEMENS_S7_PORT: int = 102

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "/app/logs/backend.log"

    # C2 Settings
    C2_SERVER_PORT: int = 4444
    IMPLANT_BEACON_INTERVAL: int = 30
    ENABLE_C2_SERVER: bool = False

    # Autonomous Settings
    AUTONOMOUS_MODE: bool = False
    AUTONOMOUS_SCAN_INTERVAL: int = 300  # 5 minutes
    AUTONOMOUS_THREAT_RESPONSE: bool = True

    # Stealth Settings
    STEALTH_MODE: bool = False
    PROCESS_INJECTION: bool = False
    ROOTKIT_MODE: bool = False

    # Persistence Settings
    PERSISTENCE_METHODS: List[str] = ["service", "scheduled_task", "registry"]
    AUTO_UPDATE: bool = False

    # WebSocket Settings
    WEBSOCKET_PING_INTERVAL: int = 20
    WEBSOCKET_PING_TIMEOUT: int = 10

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    # Backup Settings
    BACKUP_DIR: str = "/app/backups"
    BACKUP_RETENTION_DAYS: int = 30
    ENABLE_AUTO_BACKUP: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @validator("ALLOWED_EXTENSIONS", pre=True)
    def assemble_allowed_extensions(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @validator("HASH_DATABASES", pre=True)
    def assemble_hash_databases(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        return self.CORS_ORIGINS

    @property
    def ALLOWED_HOSTS(self) -> List[str]:
        if self.ENVIRONMENT == "production":
            return ["localhost", "127.0.0.1"]
        return ["*"]


# Create global settings instance
settings = Settings()

# Load environment-specific settings
if os.getenv("ENVIRONMENT") == "testing":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
elif os.getenv("ENVIRONMENT") == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    settings.CORS_ORIGINS = ["https://yourdomain.com"]