import pytest

from app.services.time_service import TimeService
from app.tools.calculator import Calculator, calculator_tool
from app.tools.registry import ToolExecutionError, ToolRegistry


@pytest.mark.asyncio
async def test_calculator_tool_executes_safe_expression() -> None:
    registry = ToolRegistry()
    registry.register(calculator_tool(Calculator()))
    assert (await registry.execute("calculate", {"expression": "452 * 89"}))["result"] == 40228


@pytest.mark.asyncio
async def test_calculator_rejects_code_execution() -> None:
    with pytest.raises(ValueError):
        await Calculator().calculate("__import__('os').system('whoami')")


@pytest.mark.asyncio
async def test_time_service_returns_requested_timezone() -> None:
    result = await TimeService().current_time("Asia/Kolkata")
    assert result["timezone"] == "Asia/Kolkata"


@pytest.mark.asyncio
async def test_unknown_tool_is_rejected() -> None:
    with pytest.raises(ToolExecutionError, match="Unknown tool"):
        await ToolRegistry().execute("unknown", {})
