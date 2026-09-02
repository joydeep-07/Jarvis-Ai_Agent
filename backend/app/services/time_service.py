from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.tools.registry import RegisteredTool


class TimeService:
    async def current_time(self, timezone: str = "UTC") -> dict[str, str]:
        try:
            current = datetime.now(ZoneInfo(timezone))
        except ZoneInfoNotFoundError as error:
            raise ValueError(f"Unknown IANA timezone: {timezone}") from error
        return {"timezone": timezone, "time": current.isoformat(), "formatted": current.strftime("%H:%M")}


def time_tool(service: TimeService) -> RegisteredTool:
    return RegisteredTool(
        name="get_time",
        description="Get the current time in an IANA timezone, such as Asia/Kolkata or UTC.",
        parameters={
            "type": "object",
            "properties": {"timezone": {"type": "string", "default": "UTC"}},
            "additionalProperties": False,
        },
        execute=service.current_time,
    )
