from fastapi import FastAPI, WebSocket


def register_realtime_handlers(app: FastAPI) -> None:
    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()
        await ws.send_json({"message": "connected"})
        await ws.close()
