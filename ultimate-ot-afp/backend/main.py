#!/usr/bin/env python3
"""
Ultimate OT-AFP (Operational Technology - Advanced Forensics Platform)
Main application entry point
"""

import uvicorn
import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import signal
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.app import create_app
from src.core.config import settings
from src.websocket.realtime import websocket_manager
from src.modules.autonomous.auto_executor import AutonomousExecutor
from src.modules.c2.c2_server import C2Server
from src.modules.stealth.stealth_operations import StealthManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global services
autonomous_executor = None
c2_server = None
stealth_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global autonomous_executor, c2_server, stealth_manager
    
    logger.info("🚀 Starting Ultimate OT-AFP Platform...")
    
    # Initialize core services
    try:
        # Initialize Stealth Manager
        stealth_manager = StealthManager()
        await stealth_manager.initialize()
        logger.info("✅ Stealth Manager initialized")
        
        # Initialize C2 Server
        c2_server = C2Server()
        await c2_server.start()
        logger.info("✅ C2 Server started")
        
        # Initialize Autonomous Executor
        autonomous_executor = AutonomousExecutor()
        await autonomous_executor.start()
        logger.info("✅ Autonomous Executor started")
        
        logger.info("🌟 Ultimate OT-AFP Platform ready!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        raise
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down Ultimate OT-AFP Platform...")
    if autonomous_executor:
        await autonomous_executor.stop()
    if c2_server:
        await c2_server.stop()
    if stealth_manager:
        await stealth_manager.cleanup()
    logger.info("👋 Ultimate OT-AFP Platform shut down")

# Create FastAPI app
app = create_app(lifespan=lifespan)

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.handle_message(websocket, data)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

# Signal handlers for graceful shutdown
def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug",
        workers=1  # Single worker for WebSocket support
    )