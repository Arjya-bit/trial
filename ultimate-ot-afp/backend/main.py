"""
Ultimate OT-AFP Platform - Main Entry Point
Advanced Forensics & Security Platform
"""
import uvicorn
from src.core.app import create_app
from src.core.config import settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )
