"""
Database connection and session management for Ultimate OT-AFP Platform
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import redis
import logging

from .config import settings


logger = logging.getLogger(__name__)

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./ot_afp.db"  # Default for development

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Redis setup
redis_client = None

def init_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.Redis.from_url(
            settings.REDIS_URL,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        # Test connection
        redis_client.ping()
        logger.info("Redis connection established successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        redis_client = None

def get_redis_client():
    """Get Redis client instance"""
    return redis_client

def init_database():
    """Initialize database and create tables"""
    try:
        # Import all models to ensure they are registered with SQLAlchemy
        from ..database.models import c2, forensics, network_security, task_manager

        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Initialize Redis
        init_redis()

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def get_db() -> Session:
    """
    Get database session
    Dependency for FastAPI routes
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database health check
async def check_database_health() -> dict:
    """Check database connectivity and health"""
    health_status = {
        "database": "healthy",
        "redis": "healthy",
        "elasticsearch": "healthy"
    }

    try:
        # Check SQL database
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
    except Exception as e:
        health_status["database"] = f"unhealthy: {str(e)}"
        logger.error(f"Database health check failed: {e}")

    try:
        # Check Redis
        if redis_client and redis_client.ping():
            pass  # Redis is healthy
        else:
            health_status["redis"] = "unhealthy: connection failed"
    except Exception as e:
        health_status["redis"] = f"unhealthy: {str(e)}"
        logger.error(f"Redis health check failed: {e}")

    try:
        # Check Elasticsearch (would need to be implemented)
        from ..database.elasticsearch_client import ElasticsearchClient
        es_client = ElasticsearchClient()
        if await es_client.ping():
            pass  # Elasticsearch is healthy
        else:
            health_status["elasticsearch"] = "unhealthy: connection failed"
    except Exception as e:
        health_status["elasticsearch"] = f"unhealthy: {str(e)}"
        logger.error(f"Elasticsearch health check failed: {e}")

    return health_status