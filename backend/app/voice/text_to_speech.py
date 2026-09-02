"""Text-to-speech provider interface and Groq-compatible implementation."""

from typing import Protocol

import httpx

from app.config import Settings


class TextToSpeechError(RuntimeError):
    """Speech audio could not be generated."""


class TextToSpeechProvider(Protocol):
    async def synthesize(self, text: str, voice: str | None = None, speed: float | None = None) -> bytes: ...


class GroqTextToSpeech:
    endpoint = "https://api.groq.com/openai/v1/audio/speech"

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self._settings = settings
        self._client = client or httpx.AsyncClient(timeout=settings.groq_timeout_seconds)
        self._owns_client = client is None

    async def synthesize(self, text: str, voice: str | None = None, speed: float | None = None) -> bytes:
        if not self._settings.groq_api_key:
            raise TextToSpeechError("GROQ_API_KEY is not configured.")
        try:
            response = await self._client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self._settings.groq_api_key}"},
                json={
                    "model": self._settings.groq_tts_model,
                    "input": text,
                    "voice": voice or self._settings.tts_voice,
                    "speed": speed or self._settings.tts_speed,
                    "response_format": "wav",
                },
            )
            response.raise_for_status()
            if not response.content:
                raise TextToSpeechError("Text-to-speech returned no audio.")
            return response.content
        except httpx.HTTPError as error:
            raise TextToSpeechError("Unable to synthesize audio with Groq.") from error

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()
