"""Energy-based voice activity detection for local speech boundaries."""

import audioop


class VoiceActivityDetector:
    """Classifies PCM16 chunks without transmitting microphone audio."""

    def __init__(self, threshold: int = 500) -> None:
        self._threshold = threshold

    def is_speech(self, pcm16: bytes) -> bool:
        if not pcm16:
            return False
        return audioop.rms(pcm16, 2) >= self._threshold
