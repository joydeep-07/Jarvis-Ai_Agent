import pytest

from app.tools.browser.browser import BrowserController


@pytest.mark.asyncio
async def test_browser_rejects_non_web_urls() -> None:
    with pytest.raises(ValueError, match="http"):
        await BrowserController().open_url("file:///sensitive.txt")
