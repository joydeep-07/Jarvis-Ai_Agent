"""Optional, local microphone recording with no persistent audio storage."""

import asyncio
import time
from collections.abc import Callable

from app.voice.vad import VoiceActivityDetector


class MicrophoneUnavailableError(RuntimeError):
    """The required local microphone runtime or device is unavailable."""


class MicrophoneRecorder:
    def __init__(self, sample_rate: int, vad: VoiceActivityDetector) -> None:
        self._sample_rate = sample_rate
        self._vad = vad

    async def record_phrase(
        self,
        silence_seconds: float,
        maximum_seconds: float,
        on_speech_start: Callable[[], None] | None = None,
    ) -> bytes:
        """Capture a phrase locally until VAD observes a silence boundary."""

        return await asyncio.to_thread(
            self._record_phrase, silence_seconds, maximum_seconds, on_speech_start
        )

    def _record_phrase(
        self,
        silence_seconds: float,
        maximum_seconds: float,
        on_speech_start: Callable[[], None] | None,
    ) -> bytes:
        try:
            import sounddevice as sd
        except ImportError as error:
            raise MicrophoneUnavailableError("Install sounddevice to use microphone recording.") from error

        chunk_frames = max(self._sample_rate // 10, 1)
        chunks: list[bytes] = []
        started = False
        silence_started: float | None = None
        deadline = time.monotonic() + maximum_seconds
        with sd.RawInputStream(samplerate=self._sample_rate, channels=1, dtype="int16") as stream:
            while time.monotonic() < deadline:
                data, _ = stream.read(chunk_frames)
                pcm = bytes(data)
                speaking = self._vad.is_speech(pcm)
                if speaking and not started:
                    started = True
                    if on_speech_start:
                        on_speech_start()
                if started:
                    chunks.append(pcm)
                    if speaking:
                        silence_started = None
                    elif silence_started is None:
                        silence_started = time.monotonic()
                    elif time.monotonic() - silence_started >= silence_seconds:
                        break
        return b"".join(chunks)
