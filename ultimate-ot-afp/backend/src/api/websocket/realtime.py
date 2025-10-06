"""
WebSocket Realtime Communication
Provides real-time updates for monitoring and alerts
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscriptions: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.active_connections.remove(websocket)
        # Remove from all subscriptions
        for topic in self.subscriptions:
            if websocket in self.subscriptions[topic]:
                self.subscriptions[topic].remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific connection"""
        await websocket.send_text(message)
    
    async def broadcast(self, message: Dict):
        """Broadcast message to all connections"""
        message_str = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
    
    async def broadcast_to_topic(self, topic: str, message: Dict):
        """Broadcast message to subscribers of a topic"""
        if topic not in self.subscriptions:
            return
        
        message_str = json.dumps(message)
        for connection in self.subscriptions[topic]:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"Error broadcasting to topic {topic}: {e}")
    
    def subscribe(self, websocket: WebSocket, topic: str):
        """Subscribe connection to a topic"""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        
        if websocket not in self.subscriptions[topic]:
            self.subscriptions[topic].append(websocket)
        
        logger.info(f"Subscribed to topic: {topic}")
    
    def unsubscribe(self, websocket: WebSocket, topic: str):
        """Unsubscribe connection from a topic"""
        if topic in self.subscriptions and websocket in self.subscriptions[topic]:
            self.subscriptions[topic].remove(websocket)
        logger.info(f"Unsubscribed from topic: {topic}")


# Global connection manager
manager = ConnectionManager()


def setup_websocket(app):
    """Setup WebSocket endpoints"""
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """Main WebSocket endpoint"""
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                msg_type = message.get("type")
                
                if msg_type == "subscribe":
                    topic = message.get("topic")
                    manager.subscribe(websocket, topic)
                    await manager.send_personal_message(
                        json.dumps({"type": "subscribed", "topic": topic}),
                        websocket
                    )
                
                elif msg_type == "unsubscribe":
                    topic = message.get("topic")
                    manager.unsubscribe(websocket, topic)
                    await manager.send_personal_message(
                        json.dumps({"type": "unsubscribed", "topic": topic}),
                        websocket
                    )
                
                elif msg_type == "ping":
                    await manager.send_personal_message(
                        json.dumps({"type": "pong"}),
                        websocket
                    )
                
                else:
                    # Echo back unknown messages
                    await manager.send_personal_message(data, websocket)
        
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            manager.disconnect(websocket)
    
    @app.websocket("/ws/alerts")
    async def alerts_websocket(websocket: WebSocket):
        """WebSocket for security alerts"""
        await manager.connect(websocket)
        manager.subscribe(websocket, "alerts")
        
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(websocket)
    
    @app.websocket("/ws/metrics")
    async def metrics_websocket(websocket: WebSocket):
        """WebSocket for system metrics"""
        await manager.connect(websocket)
        manager.subscribe(websocket, "metrics")
        
        try:
            # Send periodic updates
            while True:
                # In real implementation, fetch actual metrics
                metrics = {
                    "type": "metrics",
                    "cpu": 45.2,
                    "memory": 62.8,
                    "network": 1024
                }
                await manager.send_personal_message(json.dumps(metrics), websocket)
                await asyncio.sleep(5)
        except WebSocketDisconnect:
            manager.disconnect(websocket)


# Helper functions to send updates
async def send_alert(alert: Dict):
    """Send security alert to all subscribed clients"""
    message = {
        "type": "alert",
        "data": alert
    }
    await manager.broadcast_to_topic("alerts", message)


async def send_metric_update(metrics: Dict):
    """Send metric update to all subscribed clients"""
    message = {
        "type": "metrics",
        "data": metrics
    }
    await manager.broadcast_to_topic("metrics", message)


async def send_forensics_update(update: Dict):
    """Send forensics update"""
    message = {
        "type": "forensics",
        "data": update
    }
    await manager.broadcast_to_topic("forensics", message)


async def send_c2_update(update: Dict):
    """Send C2 update"""
    message = {
        "type": "c2",
        "data": update
    }
    await manager.broadcast_to_topic("c2", message)
