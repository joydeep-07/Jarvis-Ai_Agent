"""Focused-window operations isolated from generic input control."""

import asyncio


class WindowsWindowManager:
    def _windows(self):
        try:
            import pygetwindow
        except ImportError as error:
            raise OSError("Install pygetwindow to enable window controls.") from error
        return pygetwindow

    async def switch_window(self, title: str) -> dict[str, str]:
        def activate() -> None:
            windows = self._windows().getWindowsWithTitle(title)
            if not windows:
                raise ValueError(f"No window matching '{title}' was found.")
            windows[0].activate()

        await asyncio.to_thread(activate)
        return {"window": title, "status": "activated"}

    async def minimize_active_window(self) -> dict[str, str]:
        def minimize() -> None:
            window = self._windows().getActiveWindow()
            if not window:
                raise ValueError("There is no active window.")
            window.minimize()

        await asyncio.to_thread(minimize)
        return {"status": "minimized"}

    async def maximize_active_window(self) -> dict[str, str]:
        def maximize() -> None:
            window = self._windows().getActiveWindow()
            if not window:
                raise ValueError("There is no active window.")
            window.maximize()

        await asyncio.to_thread(maximize)
        return {"status": "maximized"}
