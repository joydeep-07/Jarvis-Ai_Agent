import pytest

from app.ai.groq_client import GroqClient, LLMProviderError
from app.config import Settings


@pytest.mark.asyncio
async def test_groq_client_requires_api_key() -> None:
    client = GroqClient(Settings(groq_api_key=None))
    with pytest.raises(LLMProviderError, match="GROQ_API_KEY"):
        await client.chat([{"role": "user", "content": "hello"}])
    await client.aclose()
