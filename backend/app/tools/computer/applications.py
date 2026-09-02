"""Configured application launching with no arbitrary command execution."""

import shlex
import subprocess

from app.config import Settings
from app.schemas.tools import PermissionLevel
from app.tools.registry import RegisteredTool


class ApplicationLauncher:
    def __init__(self, settings: Settings) -> None:
        self._commands = self._parse_commands(settings.application_commands)

    @staticmethod
    def _parse_commands(value: str) -> dict[str, str]:
        commands: dict[str, str] = {}
        if not value.strip():
            return commands
        for item in value.split(";"):
            alias, separator, command = item.partition("=")
            if not separator or not alias.strip() or not command.strip():
                raise ValueError("APPLICATION_COMMANDS must use alias=command;alias=command format.")
            commands[alias.strip().lower()] = command.strip()
        return commands

    async def launch(self, application: str) -> dict[str, int | str]:
        command = self._commands.get(application.strip().lower())
        if not command:
            configured = ", ".join(sorted(self._commands)) or "none"
            raise ValueError(f"Application is not configured. Available aliases: {configured}.")
        process = subprocess.Popen(shlex.split(command, posix=False), shell=False)  # noqa: S603
        return {"application": application, "pid": process.pid, "status": "launched"}


def application_tool(launcher: ApplicationLauncher) -> RegisteredTool:
    return RegisteredTool(
        name="open_application",
        description="Launch one of the user's configured application aliases.",
        parameters={
            "type": "object",
            "properties": {"application": {"type": "string"}},
            "required": ["application"],
            "additionalProperties": False,
        },
        execute=launcher.launch,
        permission_level=PermissionLevel.SAFE,
    )
