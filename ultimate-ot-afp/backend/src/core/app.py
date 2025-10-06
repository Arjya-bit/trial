from fastapi import FastAPI
from .config import settings
from .security import register_security
from ..api.v1.routers import api_router
from ..websocket.realtime import register_websocket


def create_app() -> FastAPI:
    application = FastAPI(title="Ultimate OT-AFP Platform", version="1.0.0")

    register_security(application)
    application.include_router(api_router, prefix="/api/v1")
    register_websocket(application)

    @application.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return application
