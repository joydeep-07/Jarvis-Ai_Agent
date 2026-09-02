from pydantic import BaseModel, Field


class CommandRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)
    conversation_id: str | None = Field(default=None, max_length=128)


class CommandResponse(BaseModel):
    conversation_id: str
    response: str
    provider: str
