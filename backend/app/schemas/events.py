from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class EventType(StrEnum):
    AI_THINKING = "AI_THINKING"
    AI_RESPONSE_STARTED = "AI_RESPONSE_STARTED"
    AI_RESPONSE_COMPLETED = "AI_RESPONSE_COMPLETED"
    ERROR = "ERROR"
    SYSTEM_STATUS_UPDATED = "SYSTEM_STATUS_UPDATED"


class AssistantEvent(BaseModel):
    type: EventType
    data: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
