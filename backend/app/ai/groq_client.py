"""Groq implementation behind a small provider boundary."""

from collections.abc import AsyncIterator
from typing import Any, Protocol

import httpx

from app.config import Settings


class LLMProvider(Protocol):
    name: str

    async def chat(self, messages: list[dict[str, str]]) -> str: ...

    async def stream(self, messages: list[dict[str, str]]) -> AsyncIterator[str]: ...


class LLMProviderError(RuntimeError):
    """An LLM provider request could not be completed safely."""


class GroqClient:
    name = "groq"
    endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self._settings = settings
        self._client = client or httpx.AsyncClient(timeout=settings.groq_timeout_seconds)
        self._owns_client = client is None

    async def chat(self, messages: list[dict[str, str]]) -> str:
        if not self._settings.groq_api_key:
            raise LLMProviderError("GROQ_API_KEY is not configured.")
        try:
            response = await self._client.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self._settings.groq_api_key}"},
                json={"model": self._settings.groq_model, "messages": messages, "temperature": 0.4},
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            if not content:
                raise LLMProviderError("Groq returned an empty response.")
            return content
        except (httpx.HTTPError, KeyError, IndexError, TypeError) as error:
            raise LLMProviderError("Unable to obtain a response from Groq.") from error

    async def stream(self, messages: list[dict[str, str]]) -> AsyncIterator[str]:
        """Stream capability is reserved for the realtime UI; chat is Phase 1's API."""
        yield await self.chat(messages)

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()
