"""
Database configuration and initialization
"""

import asyncio
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import redis.asyncio as redis
from elasticsearch import AsyncElasticsearch
import logging

from .config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async SQLAlchemy setup (if using async database)
if settings.DATABASE_URL.startswith("postgresql"):
    async_engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
    AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
else:
    async_engine = None
    AsyncSessionLocal = None

Base = declarative_base()

# Redis client
redis_client = None

# Elasticsearch client
es_client = None

async def init_database():
    """Initialize database connections"""
    global redis_client, es_client
    
    try:
        # Initialize Redis
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        await redis_client.ping()
        logger.info("✅ Redis connection established")
        
        # Initialize Elasticsearch
        es_client = AsyncElasticsearch([settings.ELASTICSEARCH_URL])
        if await es_client.ping():
            logger.info("✅ Elasticsearch connection established")
        else:
            logger.warning("⚠️ Elasticsearch connection failed")
            
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """Get async database session"""
    if AsyncSessionLocal:
        async with AsyncSessionLocal() as session:
            yield session
    else:
        raise NotImplementedError("Async database not configured")

async def get_redis():
    """Get Redis client"""
    return redis_client

async def get_elasticsearch():
    """Get Elasticsearch client"""
    return es_client

# Database models will be imported here
from ..database.models import *