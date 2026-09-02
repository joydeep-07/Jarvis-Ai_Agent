from app.schemas.tools import PermissionLevel
from app.tools.computer.controller import ComputerController
from app.tools.registry import RegisteredTool


def mouse_tools(controller: ComputerController) -> list[RegisteredTool]:
    return [
        RegisteredTool("move_mouse", "Move the pointer to screen coordinates.", {"type": "object", "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}, "duration": {"type": "number", "default": 0.2}}, "required": ["x", "y"]}, controller.move_mouse, PermissionLevel.LOW_RISK),
        RegisteredTool("click_mouse", "Click at optional screen coordinates.", {"type": "object", "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}, "button": {"type": "string", "enum": ["left", "middle", "right"], "default": "left"}}}, controller.click_mouse, PermissionLevel.LOW_RISK),
        RegisteredTool("scroll", "Scroll the focused window; positive values scroll up.", {"type": "object", "properties": {"clicks": {"type": "integer"}}, "required": ["clicks"]}, controller.scroll, PermissionLevel.LOW_RISK),
        RegisteredTool("capture_screenshot", "Capture the screen on demand without saving it.", {"type": "object", "properties": {}}, controller.capture_screenshot, PermissionLevel.LOW_RISK),
    ]
