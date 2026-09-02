from app.schemas.tools import PermissionLevel
from app.tools.computer.controller import ComputerController
from app.tools.registry import RegisteredTool


def keyboard_tools(controller: ComputerController) -> list[RegisteredTool]:
    return [
        RegisteredTool("type_text", "Type text into the focused application.", {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}, controller.type_text, PermissionLevel.LOW_RISK),
        RegisteredTool("press_key", "Press one key in the focused application.", {"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]}, controller.press_key, PermissionLevel.LOW_RISK),
        RegisteredTool("press_hotkey", "Press a keyboard shortcut in the focused application.", {"type": "object", "properties": {"keys": {"type": "array", "items": {"type": "string"}}}, "required": ["keys"]}, controller.press_hotkey, PermissionLevel.LOW_RISK),
    ]
