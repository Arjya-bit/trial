from functools import lru_cache
from typing import Optional

from elasticsearch import Elasticsearch
import redis

from src.core.config import get_settings


@lru_cache
def get_elasticsearch() -> Optional[Elasticsearch]:
    settings = get_settings()
    try:
        return Elasticsearch(settings.elasticsearch_url)
    except Exception:
        return None


@lru_cache
def get_redis() -> Optional[redis.Redis]:
    settings = get_settings()
    try:
        return redis.from_url(settings.redis_url, decode_responses=True)
    except Exception:
        return None
