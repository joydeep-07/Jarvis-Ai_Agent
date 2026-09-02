"""FastAPI composition root; feature logic remains in dedicated modules."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai import GroqClient
from app.api import command_router, health_router, websocket_router
from app.config import get_settings
from app.core.event_bus import EventBus
from app.core.lifecycle import lifespan
from app.core.orchestrator import JarvisOrchestrator
from app.memory import MemoryManager


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.settings = settings
    app.state.event_bus = EventBus()
    app.state.memory = MemoryManager()
    app.state.llm = GroqClient(settings)
    app.state.orchestrator = JarvisOrchestrator(app.state.llm, app.state.memory, app.state.event_bus)
    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(command_router, prefix=settings.api_prefix)
    app.include_router(websocket_router)
    return app


app = create_app()
