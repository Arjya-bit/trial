from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ultimate OT-AFP"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    # External services
    redis_url: str = "redis://localhost:6379/0"
    elasticsearch_url: str = "http://localhost:9200"

    # Kaggle/model config
    kaggle_dataset: Optional[str] = None  # e.g., "owner/dataset_slug"
    kaggle_download_dir: str = "models"
    model_file: Optional[str] = None  # e.g., "models/model.pkl"

    # Simple API key auth (optional)
    api_key: Optional[str] = None

    # CORS
    allow_origins: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="OTAFP_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
