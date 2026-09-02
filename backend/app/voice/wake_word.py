import re


class WakeWordDetector:
    """Text-level wake word verification after local audio capture/STT."""

    def __init__(self, wake_word: str) -> None:
        normalized = wake_word.strip().lower()
        if not normalized:
            raise ValueError("Wake word cannot be empty.")
        self._pattern = re.compile(rf"\b{re.escape(normalized)}\b", re.IGNORECASE)

    def detected(self, text: str) -> bool:
        return bool(self._pattern.search(text))

    def remove(self, text: str) -> str:
        return self._pattern.sub("", text, count=1).strip(" ,.!?")
