from app.schemas.tools import PermissionLevel
from app.tools.computer.windows_manager import WindowsWindowManager
from app.tools.registry import RegisteredTool


def window_tools(manager: WindowsWindowManager) -> list[RegisteredTool]:
    return [
        RegisteredTool("switch_window", "Activate a desktop window by title.", {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]}, manager.switch_window, PermissionLevel.LOW_RISK),
        RegisteredTool("minimize_window", "Minimize the active desktop window.", {"type": "object", "properties": {}}, manager.minimize_active_window, PermissionLevel.LOW_RISK),
        RegisteredTool("maximize_window", "Maximize the active desktop window.", {"type": "object", "properties": {}}, manager.maximize_active_window, PermissionLevel.LOW_RISK),
    ]
