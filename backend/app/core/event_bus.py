"""Asynchronous in-process event fan-out for API and WebSocket consumers."""

import asyncio
from collections.abc import AsyncIterator

from app.schemas.events import AssistantEvent


class EventBus:
    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue[AssistantEvent]] = set()

    async def publish(self, event: AssistantEvent) -> None:
        for subscriber in tuple(self._subscribers):
            subscriber.put_nowait(event)

    async def subscribe(self) -> AsyncIterator[AssistantEvent]:
        queue: asyncio.Queue[AssistantEvent] = asyncio.Queue(maxsize=100)
        self._subscribers.add(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            self._subscribers.discard(queue)
