"""
WebSocket Real-time Communication Handler
"""

import asyncio
import json
import logging
from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[WebSocket, Dict] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str = None):
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if user_id:
            self.user_connections[user_id] = websocket
        
        # Store connection metadata
        self.connection_metadata[websocket] = {
            "connected_at": datetime.now(),
            "user_id": user_id,
            "message_count": 0
        }
        
        logger.info(f"🔌 WebSocket connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "timestamp": datetime.now().isoformat(),
            "message": "Connected to Ultimate OT-AFP Platform"
        }, websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        try:
            self.active_connections.remove(websocket)
            
            # Remove from user connections
            user_id = None
            for uid, ws in list(self.user_connections.items()):
                if ws == websocket:
                    user_id = uid
                    del self.user_connections[uid]
                    break
            
            # Remove metadata
            if websocket in self.connection_metadata:
                del self.connection_metadata[websocket]
            
            logger.info(f"🔌 WebSocket disconnected (user: {user_id}). Total connections: {len(self.active_connections)}")
            
        except ValueError:
            pass  # Connection already removed
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(json.dumps(message))
            
            # Update message count
            if websocket in self.connection_metadata:
                self.connection_metadata[websocket]["message_count"] += 1
                
        except Exception as e:
            logger.error(f"❌ Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def send_to_user(self, message: dict, user_id: str):
        """Send message to specific user"""
        if user_id in self.user_connections:
            await self.send_personal_message(message, self.user_connections[user_id])
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        # Add timestamp to message
        message["broadcast_timestamp"] = datetime.now().isoformat()
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
                
                # Update message count
                if connection in self.connection_metadata:
                    self.connection_metadata[connection]["message_count"] += 1
                    
            except Exception as e:
                logger.error(f"❌ Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
        
        logger.debug(f"📡 Broadcast sent to {len(self.active_connections)} connections")
    
    async def handle_message(self, websocket: WebSocket, data: str):
        """Handle incoming WebSocket message"""
        try:
            message = json.loads(data)
            message_type = message.get("type")
            
            # Update message count
            if websocket in self.connection_metadata:
                self.connection_metadata[websocket]["message_count"] += 1
            
            # Handle different message types
            if message_type == "ping":
                await self.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }, websocket)
            
            elif message_type == "subscribe":
                await self._handle_subscription(websocket, message)
            
            elif message_type == "unsubscribe":
                await self._handle_unsubscription(websocket, message)
            
            elif message_type == "get_status":
                await self._handle_status_request(websocket, message)
            
            else:
                logger.warning(f"⚠️ Unknown message type: {message_type}")
                await self.send_personal_message({
                    "type": "error",
                    "message": f"Unknown message type: {message_type}"
                }, websocket)
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON message: {e}")
            await self.send_personal_message({
                "type": "error",
                "message": "Invalid JSON format"
            }, websocket)
        
        except Exception as e:
            logger.error(f"❌ Error handling message: {e}")
            await self.send_personal_message({
                "type": "error", 
                "message": "Message processing error"
            }, websocket)
    
    async def _handle_subscription(self, websocket: WebSocket, message: dict):
        """Handle subscription requests"""
        topic = message.get("topic")
        
        if not topic:
            await self.send_personal_message({
                "type": "error",
                "message": "Topic is required for subscription"
            }, websocket)
            return
        
        # Add subscription to metadata
        if websocket not in self.connection_metadata:
            return
        
        if "subscriptions" not in self.connection_metadata[websocket]:
            self.connection_metadata[websocket]["subscriptions"] = set()
        
        self.connection_metadata[websocket]["subscriptions"].add(topic)
        
        await self.send_personal_message({
            "type": "subscription_confirmed",
            "topic": topic,
            "message": f"Subscribed to {topic}"
        }, websocket)
        
        logger.info(f"📡 Client subscribed to topic: {topic}")
    
    async def _handle_unsubscription(self, websocket: WebSocket, message: dict):
        """Handle unsubscription requests"""
        topic = message.get("topic")
        
        if websocket in self.connection_metadata and "subscriptions" in self.connection_metadata[websocket]:
            self.connection_metadata[websocket]["subscriptions"].discard(topic)
        
        await self.send_personal_message({
            "type": "unsubscription_confirmed", 
            "topic": topic,
            "message": f"Unsubscribed from {topic}"
        }, websocket)
        
        logger.info(f"📡 Client unsubscribed from topic: {topic}")
    
    async def _handle_status_request(self, websocket: WebSocket, message: dict):
        """Handle status information requests"""
        metadata = self.connection_metadata.get(websocket, {})
        
        status = {
            "type": "status_response",
            "connection_info": {
                "connected_at": metadata.get("connected_at", "").isoformat() if metadata.get("connected_at") else "",
                "message_count": metadata.get("message_count", 0),
                "subscriptions": list(metadata.get("subscriptions", set())),
                "user_id": metadata.get("user_id")
            },
            "server_info": {
                "total_connections": len(self.active_connections),
                "server_timestamp": datetime.now().isoformat()
            }
        }
        
        await self.send_personal_message(status, websocket)
    
    async def send_to_topic_subscribers(self, topic: str, message: dict):
        """Send message to all subscribers of a specific topic"""
        message["topic"] = topic
        subscribers = []
        
        for websocket, metadata in self.connection_metadata.items():
            subscriptions = metadata.get("subscriptions", set())
            if topic in subscriptions:
                subscribers.append(websocket)
        
        if not subscribers:
            return
        
        disconnected = []
        for websocket in subscribers:
            try:
                await self.send_personal_message(message, websocket)
            except Exception as e:
                logger.error(f"❌ Error sending to subscriber: {e}")
                disconnected.append(websocket)
        
        # Clean up disconnected connections
        for websocket in disconnected:
            self.disconnect(websocket)
        
        logger.debug(f"📡 Sent message to {len(subscribers)} subscribers of topic '{topic}'")
    
    async def send_forensics_update(self, case_id: str, update_data: dict):
        """Send forensics case update"""
        message = {
            "type": "forensics_update",
            "case_id": case_id,
            "data": update_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_to_topic_subscribers("forensics", message)
    
    async def send_network_alert(self, alert_data: dict):
        """Send network security alert"""
        message = {
            "type": "network_alert",
            "severity": alert_data.get("severity", "medium"),
            "data": alert_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_to_topic_subscribers("network_security", message)
    
    async def send_ot_event(self, device_id: str, event_data: dict):
        """Send OT security event"""
        message = {
            "type": "ot_event",
            "device_id": device_id,
            "data": event_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_to_topic_subscribers("ot_security", message)
    
    async def send_ai_analysis_result(self, analysis_type: str, result_data: dict):
        """Send AI analysis result"""
        message = {
            "type": "ai_analysis_result",
            "analysis_type": analysis_type,
            "data": result_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_to_topic_subscribers("ai_analysis", message)
    
    async def send_system_metrics(self, metrics_data: dict):
        """Send system metrics update"""
        message = {
            "type": "system_metrics",
            "data": metrics_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_to_topic_subscribers("system_metrics", message)
    
    async def send_task_update(self, task_id: str, status: str, result: dict = None):
        """Send task execution update"""
        message = {
            "type": "task_update",
            "task_id": task_id,
            "status": status,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        await self.send_to_topic_subscribers("tasks", message)
    
    def get_connection_stats(self) -> dict:
        """Get WebSocket connection statistics"""
        total_connections = len(self.active_connections)
        user_connections = len(self.user_connections)
        total_messages = sum(
            metadata.get("message_count", 0) 
            for metadata in self.connection_metadata.values()
        )
        
        subscriptions_by_topic = {}
        for metadata in self.connection_metadata.values():
            for topic in metadata.get("subscriptions", set()):
                subscriptions_by_topic[topic] = subscriptions_by_topic.get(topic, 0) + 1
        
        return {
            "total_connections": total_connections,
            "authenticated_connections": user_connections,
            "anonymous_connections": total_connections - user_connections,
            "total_messages_processed": total_messages,
            "subscriptions_by_topic": subscriptions_by_topic,
            "uptime": datetime.now().isoformat()
        }

# Global WebSocket manager instance
websocket_manager = WebSocketManager()