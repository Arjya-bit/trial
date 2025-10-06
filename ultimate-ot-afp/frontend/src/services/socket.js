export function connectRealtime() {
  const ws = new WebSocket('ws://localhost:8000/ws/realtime');
  ws.onopen = () => console.log('WebSocket connected');
  ws.onmessage = (e) => console.log('Realtime:', e.data);
  return ws;
}
