"""
WebSocket service for React frontend
"""

import io from 'socket.io-client';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.eventHandlers = new Map();
  }

  connect(url = 'ws://localhost:8000/ws') {
    try {
      this.socket = io(url, {
        transports: ['websocket'],
        upgrade: true,
        rememberUpgrade: true,
        timeout: 5000,
        forceNew: true
      });

      this.setupEventHandlers();
      
      return this.socket;
    } catch (error) {
      console.error('WebSocket connection error:', error);
      return null;
    }
  }

  setupEventHandlers() {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      console.log('🔌 WebSocket connected');
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.emit('connection_status', { connected: true });
    });

    this.socket.on('disconnect', (reason) => {
      console.log('🔌 WebSocket disconnected:', reason);
      this.isConnected = false;
      this.emit('connection_status', { connected: false, reason });
      
      if (reason === 'io server disconnect') {
        // Server initiated disconnect, don't reconnect
        return;
      }
      
      this.attemptReconnection();
    });

    this.socket.on('connect_error', (error) => {
      console.error('🔌 WebSocket connection error:', error);
      this.isConnected = false;
      this.emit('connection_error', error);
      this.attemptReconnection();
    });

    // Handle custom events
    this.socket.on('forensics_update', (data) => {
      this.emit('forensics_update', data);
    });

    this.socket.on('network_alert', (data) => {
      this.emit('network_alert', data);
    });

    this.socket.on('ot_event', (data) => {
      this.emit('ot_event', data);
    });

    this.socket.on('ai_analysis_result', (data) => {
      this.emit('ai_analysis_result', data);
    });

    this.socket.on('system_metrics', (data) => {
      this.emit('system_metrics', data);
    });

    this.socket.on('task_update', (data) => {
      this.emit('task_update', data);
    });

    this.socket.on('security_alert', (data) => {
      this.emit('security_alert', data);
    });
  }

  attemptReconnection() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log('❌ Max reconnection attempts reached');
      this.emit('reconnection_failed');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`🔄 Attempting reconnection ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${delay}ms`);
    
    setTimeout(() => {
      if (!this.isConnected) {
        this.socket?.connect();
      }
    }, delay);
  }

  subscribe(topic) {
    if (!this.isConnected || !this.socket) {
      console.warn('⚠️ Cannot subscribe: WebSocket not connected');
      return false;
    }

    this.socket.emit('message', JSON.stringify({
      type: 'subscribe',
      topic: topic
    }));

    console.log(`📡 Subscribed to topic: ${topic}`);
    return true;
  }

  unsubscribe(topic) {
    if (!this.isConnected || !this.socket) {
      console.warn('⚠️ Cannot unsubscribe: WebSocket not connected');
      return false;
    }

    this.socket.emit('message', JSON.stringify({
      type: 'unsubscribe',
      topic: topic
    }));

    console.log(`📡 Unsubscribed from topic: ${topic}`);
    return true;
  }

  sendMessage(message) {
    if (!this.isConnected || !this.socket) {
      console.warn('⚠️ Cannot send message: WebSocket not connected');
      return false;
    }

    this.socket.emit('message', JSON.stringify(message));
    return true;
  }

  ping() {
    return this.sendMessage({ type: 'ping' });
  }

  getStatus() {
    return this.sendMessage({ type: 'get_status' });
  }

  // Event handling
  on(event, handler) {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, []);
    }
    this.eventHandlers.get(event).push(handler);
    
    // Also listen on socket if connected
    if (this.socket) {
      this.socket.on(event, handler);
    }
  }

  off(event, handler) {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
    
    // Also remove from socket
    if (this.socket) {
      this.socket.off(event, handler);
    }
  }

  emit(event, data) {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error(`Error in event handler for ${event}:`, error);
        }
      });
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
    this.isConnected = false;
    this.reconnectAttempts = 0;
  }

  getConnectionInfo() {
    return {
      connected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      maxReconnectAttempts: this.maxReconnectAttempts,
      socketId: this.socket?.id || null
    };
  }
}

// Create singleton instance
const websocketService = new WebSocketService();

// Initialize WebSocket connection
export const initializeWebSocket = () => {
  return websocketService.connect();
};

// Export service for direct use
export default websocketService;