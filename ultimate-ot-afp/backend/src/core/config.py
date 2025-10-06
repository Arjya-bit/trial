"""
Configuration Management
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    PROJECT_NAME: str = "Ultimate OT-AFP Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=True)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    WORKERS: int = Field(default=4)
    LOG_LEVEL: str = Field(default="INFO")
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )
    
    # Database - PostgreSQL
    POSTGRES_USER: str = Field(default="otafp_user")
    POSTGRES_PASSWORD: str = Field(default="otafp_password")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default="otafp_db")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_PASSWORD: str = Field(default="")
    
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Elasticsearch
    ELASTICSEARCH_HOST: str = Field(default="localhost")
    ELASTICSEARCH_PORT: int = Field(default=9200)
    ELASTICSEARCH_USER: str = Field(default="elastic")
    ELASTICSEARCH_PASSWORD: str = Field(default="changeme")
    
    @property
    def ELASTICSEARCH_URL(self) -> str:
        return f"http://{self.ELASTICSEARCH_USER}:{self.ELASTICSEARCH_PASSWORD}@{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}"
    
    # AI Model
    AI_MODEL_PATH: str = Field(default="./models")
    KAGGLE_USERNAME: str = Field(default="")
    KAGGLE_KEY: str = Field(default="")
    AI_MODEL_DATASET: str = Field(default="lakshmi25npathi/cybersecurity-incidents")
    
    # C2 Settings
    C2_PORT: int = Field(default=8443)
    C2_SSL_CERT: str = Field(default="./certs/cert.pem")
    C2_SSL_KEY: str = Field(default="./certs/key.pem")
    
    # Forensics
    FORENSICS_STORAGE_PATH: str = Field(default="./forensics_data")
    MAX_UPLOAD_SIZE: int = Field(default=5368709120)  # 5GB
    
    # OT Security
    OT_PROTOCOLS: List[str] = Field(
        default=["modbus", "s7comm", "opcua", "dnp3", "bacnet"]
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
