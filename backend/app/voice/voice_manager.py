"""Asynchronous voice pipeline coordinator."""

from app.config import Settings
from app.core.event_bus import EventBus
from app.schemas.events import AssistantEvent, EventType
from app.voice.microphone import MicrophoneRecorder
from app.voice.speech_to_text import SpeechToTextProvider
from app.voice.text_to_speech import TextToSpeechProvider
from app.voice.wake_word import WakeWordDetector


class VoiceManager:
    def __init__(
        self,
        settings: Settings,
        events: EventBus,
        speech_to_text: SpeechToTextProvider,
        text_to_speech: TextToSpeechProvider,
        recorder: MicrophoneRecorder,
    ) -> None:
        self._settings = settings
        self._events = events
        self._speech_to_text = speech_to_text
        self._text_to_speech = text_to_speech
        self._recorder = recorder
        self._wake_word = WakeWordDetector(settings.wake_word)

    async def transcribe(self, audio: bytes, filename: str, content_type: str) -> tuple[str, bool]:
        await self._events.publish(AssistantEvent(type=EventType.TRANSCRIPTION_STARTED))
        text = await self._speech_to_text.transcribe(audio, filename, content_type)
        detected = self._wake_word.detected(text)
        if self._settings.wake_word_enabled and not detected:
            return "", False
        if detected:
            await self._events.publish(AssistantEvent(type=EventType.WAKE_WORD_DETECTED))
            text = self._wake_word.remove(text)
        await self._events.publish(
            AssistantEvent(type=EventType.TRANSCRIPTION_COMPLETED, data={"text": text})
        )
        return text, detected

    async def speak(self, text: str, voice: str | None = None, speed: float | None = None) -> bytes:
        await self._events.publish(AssistantEvent(type=EventType.TTS_STARTED))
        audio = await self._text_to_speech.synthesize(text, voice, speed)
        await self._events.publish(AssistantEvent(type=EventType.TTS_COMPLETED))
        return audio

    async def listen_once(self) -> tuple[str, bool]:
        await self._events.publish(AssistantEvent(type=EventType.USER_STARTED_SPEAKING))
        audio = await self._recorder.record_phrase(
            self._settings.voice_silence_seconds, self._settings.voice_max_recording_seconds
        )
        await self._events.publish(AssistantEvent(type=EventType.USER_STOPPED_SPEAKING))
        return await self.transcribe(audio, "microphone.wav", "audio/wav")
