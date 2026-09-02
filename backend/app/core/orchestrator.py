"""Coordinates user input, the LLM provider, memory, and UI events."""

from uuid import uuid4

import json
from typing import Any

from app.ai.groq_client import LLMProvider, LLMProviderError
from app.ai.prompts import build_system_prompt
from app.core.event_bus import EventBus
from app.memory import MemoryManager
from app.schemas.events import AssistantEvent, EventType
from app.tools.registry import ToolExecutionError, ToolRegistry


class JarvisOrchestrator:
    def __init__(
        self,
        llm: LLMProvider,
        memory: MemoryManager,
        events: EventBus,
        tools: ToolRegistry | None = None,
        max_iterations: int = 6,
    ) -> None:
        self._llm = llm
        self._memory = memory
        self._events = events
        self._tools = tools or ToolRegistry()
        self._max_iterations = max_iterations

    async def respond(self, message: str, conversation_id: str | None = None) -> tuple[str, str]:
        session_id = conversation_id or str(uuid4())
        conversation = self._memory.conversation(session_id)
        conversation.add("user", message)
        await self._events.publish(AssistantEvent(type=EventType.AI_THINKING))
        try:
            response = await self._run_agent([{"role": "system", "content": build_system_prompt()}, *conversation.history()])
        except LLMProviderError as error:
            await self._events.publish(AssistantEvent(type=EventType.ERROR, data={"message": str(error)}))
            raise
        conversation.add("assistant", response)
        await self._events.publish(AssistantEvent(type=EventType.AI_RESPONSE_COMPLETED, data={"response": response}))
        return session_id, response

    async def _run_agent(self, messages: list[dict[str, Any]]) -> str:
        complete = getattr(self._llm, "complete", None)
        if complete is None:
            return await self._llm.chat(messages)
        for _ in range(self._max_iterations):
            completion = await complete(messages, self._tools.definitions())
            if not completion.tool_calls:
                return completion.content or "I was unable to prepare a response."
            messages.append(
                {
                    "role": "assistant",
                    "content": completion.content,
                    "tool_calls": [
                        {"id": call.id, "type": "function", "function": {"name": call.name, "arguments": json.dumps(call.arguments)}}
                        for call in completion.tool_calls
                    ],
                }
            )
            for call in completion.tool_calls:
                await self._events.publish(AssistantEvent(type=EventType.TOOL_STARTED, data={"tool": call.name}))
                try:
                    result = await self._tools.execute(call.name, call.arguments)
                    await self._events.publish(AssistantEvent(type=EventType.TOOL_COMPLETED, data={"tool": call.name}))
                except ToolExecutionError as error:
                    result = {"error": str(error)}
                    await self._events.publish(AssistantEvent(type=EventType.TOOL_FAILED, data={"tool": call.name}))
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        return "I reached the maximum number of safe steps for this request."
