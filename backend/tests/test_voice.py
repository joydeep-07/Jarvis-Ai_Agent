import pytest

from app.config import Settings
from app.core.event_bus import EventBus
from app.voice.vad import VoiceActivityDetector
from app.voice.voice_manager import VoiceManager


class FakeStt:
    async def transcribe(self, audio: bytes, filename: str, content_type: str) -> str:
        return "Jarvis, tell me the time"


class FakeTts:
    async def synthesize(self, text: str, voice=None, speed=None) -> bytes:
        return b"RIFFfake-wav"


class NoopRecorder:
    async def record_phrase(self, *args, **kwargs) -> bytes:
        return b"audio"


@pytest.mark.asyncio
async def test_voice_manager_removes_wake_word() -> None:
    settings = Settings(groq_api_key="test", wake_word_enabled=True)
    manager = VoiceManager(settings, EventBus(), FakeStt(), FakeTts(), NoopRecorder())
    text, detected = await manager.transcribe(b"audio", "clip.wav", "audio/wav")
    assert detected is True
    assert text == "tell me the time"


@pytest.mark.asyncio
async def test_voice_manager_synthesizes_audio() -> None:
    settings = Settings(groq_api_key="test")
    manager = VoiceManager(settings, EventBus(), FakeStt(), FakeTts(), NoopRecorder())
    assert await manager.speak("Hello") == b"RIFFfake-wav"


def test_vad_detects_non_silent_pcm() -> None:
    assert VoiceActivityDetector(threshold=10).is_speech(b"\xff\x7f" * 20)
