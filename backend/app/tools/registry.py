"""Dynamic tool discovery and execution boundary."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from app.schemas.tools import PermissionLevel

ToolExecutor = Callable[..., Awaitable[dict[str, Any]]]


class ToolExecutionError(RuntimeError):
    """A registered tool could not complete its requested operation."""


@dataclass(frozen=True)
class RegisteredTool:
    name: str
    description: str
    parameters: dict[str, Any]
    execute: ToolExecutor
    permission_level: PermissionLevel = PermissionLevel.SAFE
    confirmation_required: bool = False

    def as_llm_tool(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(self, tool: RegisteredTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def definitions(self) -> list[dict[str, Any]]:
        return [tool.as_llm_tool() for tool in self._tools.values()]

    async def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        tool = self._tools.get(name)
        if not tool:
            raise ToolExecutionError(f"Unknown tool: {name}")
        if tool.permission_level == PermissionLevel.BLOCKED:
            raise ToolExecutionError(f"Tool '{name}' is blocked by policy.")
        if tool.confirmation_required:
            raise ToolExecutionError(f"Tool '{name}' requires user confirmation.")
        try:
            return await tool.execute(**arguments)
        except (TypeError, ValueError, OSError) as error:
            raise ToolExecutionError(f"Tool '{name}' could not complete: {error}") from error
