from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.llm.aclose()
    await app.state.speech_to_text.aclose()
    await app.state.text_to_speech.aclose()
