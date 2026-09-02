from pydantic import BaseModel, Field


class SpeakRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)
    voice: str | None = Field(default=None, max_length=64)
    speed: float | None = Field(default=None, ge=0.5, le=2.0)


class TranscriptionResponse(BaseModel):
    text: str
    wake_word_detected: bool
