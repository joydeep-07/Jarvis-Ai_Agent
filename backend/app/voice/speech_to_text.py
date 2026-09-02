"""Speech-to-text provider interface and Groq implementation."""

from typing import Protocol

import httpx

from app.config import Settings


class SpeechRecognitionError(RuntimeError):
    """Speech could not be transcribed."""


class SpeechToTextProvider(Protocol):
    async def transcribe(self, audio: bytes, filename: str, content_type: str) -> str: ...


class GroqSpeechToText:
    endpoint = "https://api.groq.com/openai/v1/audio/transcriptions"

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self._settings = settings
        self._client = client or httpx.AsyncClient(timeout=settings.groq_timeout_seconds)
        self._owns_client = client is None

    async def transcribe(self, audio: bytes, filename: str, content_type: str) -> str:
        if not audio:
            raise SpeechRecognitionError("No audio was provided.")
        if not self._settings.groq_api_key:
            raise SpeechRecognitionError("GROQ_API_KEY is not configured.")
        try:
            response = await self._client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self._settings.groq_api_key}"},
                data={"model": self._settings.groq_stt_model},
                files={"file": (filename, audio, content_type)},
            )
            response.raise_for_status()
            text = response.json()["text"].strip()
            if not text:
                raise SpeechRecognitionError("Speech recognition returned no text.")
            return text
        except (httpx.HTTPError, KeyError, TypeError) as error:
            raise SpeechRecognitionError("Unable to transcribe audio with Groq.") from error

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()
