"""
Redis Client Configuration
"""
import redis.asyncio as redis
from typing import Optional
from ..core.config import settings

redis_client: Optional[redis.Redis] = None


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    redis_client = await redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=50
    )
    print("✅ Redis connected")


async def close_redis():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()
        print("✅ Redis disconnected")


async def get_redis() -> redis.Redis:
    """Get Redis client"""
    return redis_client


# Cache operations
async def cache_set(key: str, value: str, expire: int = 3600):
    """Set cache value"""
    if redis_client:
        await redis_client.setex(key, expire, value)


async def cache_get(key: str) -> Optional[str]:
    """Get cache value"""
    if redis_client:
        return await redis_client.get(key)
    return None


async def cache_delete(key: str):
    """Delete cache key"""
    if redis_client:
        await redis_client.delete(key)
