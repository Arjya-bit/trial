from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.api.v1.routers import api_router
from src.websocket.realtime import register_realtime_handlers


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    # WebSocket handlers
    register_realtime_handlers(app)

    @app.get("/healthz")
    def healthcheck():
        return {"status": "ok", "app": settings.app_name}

    return app
