"""Coordinates user input, the LLM provider, memory, and UI events."""

from uuid import uuid4

from app.ai.groq_client import LLMProvider, LLMProviderError
from app.ai.prompts import build_system_prompt
from app.core.event_bus import EventBus
from app.memory import MemoryManager
from app.schemas.events import AssistantEvent, EventType


class JarvisOrchestrator:
    def __init__(self, llm: LLMProvider, memory: MemoryManager, events: EventBus) -> None:
        self._llm = llm
        self._memory = memory
        self._events = events

    async def respond(self, message: str, conversation_id: str | None = None) -> tuple[str, str]:
        session_id = conversation_id or str(uuid4())
        conversation = self._memory.conversation(session_id)
        conversation.add("user", message)
        await self._events.publish(AssistantEvent(type=EventType.AI_THINKING))
        try:
            response = await self._llm.chat(
                [{"role": "system", "content": build_system_prompt()}, *conversation.history()]
            )
        except LLMProviderError as error:
            await self._events.publish(AssistantEvent(type=EventType.ERROR, data={"message": str(error)}))
            raise
        conversation.add("assistant", response)
        await self._events.publish(AssistantEvent(type=EventType.AI_RESPONSE_COMPLETED, data={"response": response}))
        return session_id, response
