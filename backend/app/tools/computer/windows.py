"""Windows implementation using PyAutoGUI; all calls run off the event loop."""

import asyncio


class WindowsComputerController:
    def _pyautogui(self):
        try:
            import pyautogui
        except ImportError as error:
            raise OSError("Install pyautogui to enable computer controls.") from error
        pyautogui.FAILSAFE = True
        return pyautogui

    async def type_text(self, text: str) -> dict[str, str]:
        await asyncio.to_thread(self._pyautogui().write, text, interval=0.01)
        return {"status": "typed"}

    async def press_key(self, key: str) -> dict[str, str]:
        await asyncio.to_thread(self._pyautogui().press, key)
        return {"key": key, "status": "pressed"}

    async def press_hotkey(self, keys: list[str]) -> dict[str, list[str]]:
        if not keys:
            raise ValueError("At least one key is required.")
        await asyncio.to_thread(self._pyautogui().hotkey, *keys)
        return {"keys": keys, "status": ["pressed"]}

    async def move_mouse(self, x: int, y: int, duration: float = 0.2) -> dict[str, int]:
        await asyncio.to_thread(self._pyautogui().moveTo, x, y, duration)
        return {"x": x, "y": y}

    async def click_mouse(
        self, x: int | None = None, y: int | None = None, button: str = "left"
    ) -> dict[str, str]:
        if button not in {"left", "middle", "right"}:
            raise ValueError("Button must be left, middle, or right.")
        await asyncio.to_thread(self._pyautogui().click, x, y, button=button)
        return {"button": button, "status": "clicked"}

    async def scroll(self, clicks: int) -> dict[str, int]:
        await asyncio.to_thread(self._pyautogui().scroll, clicks)
        return {"clicks": clicks}

    async def capture_screenshot(self) -> dict[str, int | str]:
        """Capture on demand, then immediately discard pixels after reading dimensions."""

        image = await asyncio.to_thread(self._pyautogui().screenshot)
        width, height = image.size
        return {"width": width, "height": height, "status": "captured_not_stored"}
