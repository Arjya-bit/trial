"""
Database Configuration and Management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

# SQLAlchemy Base
Base = declarative_base()

# Async Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=10,
    max_overflow=20
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncSession:
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_databases():
    """Initialize all database connections"""
    from ..database.redis_client import init_redis
    from ..database.elasticsearch_client import init_elasticsearch
    
    # Initialize PostgreSQL tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize Redis
    await init_redis()
    
    # Initialize Elasticsearch
    await init_elasticsearch()


async def close_databases():
    """Close all database connections"""
    from ..database.redis_client import close_redis
    from ..database.elasticsearch_client import close_elasticsearch
    
    await engine.dispose()
    await close_redis()
    await close_elasticsearch()
