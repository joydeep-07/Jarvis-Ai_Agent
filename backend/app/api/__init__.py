from app.api.health import router as health_router
from app.api.routes import router as command_router
from app.api.websocket import router as websocket_router
from app.api.voice import router as voice_router

__all__ = ["command_router", "health_router", "voice_router", "websocket_router"]
