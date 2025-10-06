from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Ultimate OT-AFP Platform"
    environment: str = "development"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60

    redis_url: str = "redis://localhost:6379/0"
    elastic_url: str = "http://localhost:9200"

    kaggle_username: str | None = None
    kaggle_key: str | None = None
    kaggle_dataset: str | None = None  # e.g. "owner/dataset"
    kaggle_model_file: str | None = None  # e.g. "model.joblib"

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
