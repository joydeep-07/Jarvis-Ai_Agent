import pytest
from app.core.event_bus import EventBus
from app.core.orchestrator import JarvisOrchestrator
from app.memory import MemoryManager


class FakeProvider:
    name = "fake"

    async def chat(self, messages: list[dict[str, str]]) -> str:
        return f"Acknowledged: {messages[-1]['content']}"


@pytest.fixture
def orchestrator() -> JarvisOrchestrator:
    return JarvisOrchestrator(FakeProvider(), MemoryManager(), EventBus())
