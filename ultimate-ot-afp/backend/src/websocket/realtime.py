from fastapi import FastAPI, WebSocket, WebSocketDisconnect


def register_websocket(app: FastAPI) -> None:
    @app.websocket("/ws/realtime")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            await websocket.send_json({"message": "connected"})
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(f"echo: {data}")
        except WebSocketDisconnect:
            pass
