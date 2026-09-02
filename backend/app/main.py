"""FastAPI composition root; feature logic remains in dedicated modules."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai import GroqClient
from app.api import command_router, health_router, voice_router, websocket_router
from app.config import get_settings
from app.core.event_bus import EventBus
from app.core.lifecycle import lifespan
from app.core.orchestrator import JarvisOrchestrator
from app.memory import MemoryManager
from app.services.time_service import TimeService, time_tool
from app.tools.calculator import Calculator, calculator_tool
from app.tools.browser.browser import BrowserController
from app.tools.browser.navigation import browser_tools
from app.tools.computer.applications import ApplicationLauncher, application_tool
from app.tools.computer.keyboard import keyboard_tools
from app.tools.computer.mouse import mouse_tools
from app.tools.computer.windows import WindowsComputerController
from app.tools.computer.windows_manager import WindowsWindowManager
from app.tools.computer.windows_tools import window_tools
from app.tools.registry import ToolRegistry
from app.voice.microphone import MicrophoneRecorder
from app.voice.speech_to_text import GroqSpeechToText
from app.voice.text_to_speech import GroqTextToSpeech
from app.voice.vad import VoiceActivityDetector
from app.voice.voice_manager import VoiceManager


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
    app.state.speech_to_text = GroqSpeechToText(settings)
    app.state.text_to_speech = GroqTextToSpeech(settings)
    app.state.voice_manager = VoiceManager(
        settings,
        app.state.event_bus,
        app.state.speech_to_text,
        app.state.text_to_speech,
        MicrophoneRecorder(settings.voice_sample_rate, VoiceActivityDetector()),
    )
    app.state.tools = ToolRegistry()
    app.state.tools.register(calculator_tool(Calculator()))
    app.state.tools.register(time_tool(TimeService()))
    app.state.tools.register(application_tool(ApplicationLauncher(settings)))
    computer = WindowsComputerController()
    for tool in [
        *keyboard_tools(computer),
        *mouse_tools(computer),
        *window_tools(WindowsWindowManager()),
        *browser_tools(BrowserController()),
    ]:
        app.state.tools.register(tool)
    app.state.orchestrator = JarvisOrchestrator(
        app.state.llm,
        app.state.memory,
        app.state.event_bus,
        app.state.tools,
        settings.max_agent_iterations,
    )
    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(command_router, prefix=settings.api_prefix)
    app.include_router(voice_router, prefix=settings.api_prefix)
    app.include_router(websocket_router)
    return app


app = create_app()
