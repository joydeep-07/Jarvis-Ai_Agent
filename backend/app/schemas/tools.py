from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class PermissionLevel(StrEnum):
    SAFE = "SAFE"
    LOW_RISK = "LOW_RISK"
    CONFIRM_REQUIRED = "CONFIRM_REQUIRED"
    HIGH_RISK = "HIGH_RISK"
    BLOCKED = "BLOCKED"


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class LLMCompletion(BaseModel):
    content: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
