from app.schemas.tools import PermissionLevel
from app.tools.browser.browser import BrowserController
from app.tools.registry import RegisteredTool


def browser_tools(controller: BrowserController) -> list[RegisteredTool]:
    return [
        RegisteredTool("open_url", "Open a validated web URL in the default browser.", {"type": "object", "properties": {"url": {"type": "string", "format": "uri"}}, "required": ["url"]}, controller.open_url, PermissionLevel.SAFE)
    ]
