"""Default-browser actions with strict URL validation."""

import asyncio
import webbrowser
from urllib.parse import urlparse


class BrowserController:
    async def open_url(self, url: str) -> dict[str, str]:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Only valid http and https URLs can be opened.")
        opened = await asyncio.to_thread(webbrowser.open, url, new=2)
        if not opened:
            raise OSError("The default browser could not open the URL.")
        return {"url": url, "status": "opened"}
