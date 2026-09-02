from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import Response

from app.schemas.voice import SpeakRequest, TranscriptionResponse
from app.schemas.commands import CommandResponse
from app.ai.groq_client import LLMProviderError
from app.voice.speech_to_text import SpeechRecognitionError
from app.voice.text_to_speech import TextToSpeechError

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/transcriptions", response_model=TranscriptionResponse)
async def transcribe(request: Request, file: UploadFile = File(...)) -> TranscriptionResponse:
    try:
        text, detected = await request.app.state.voice_manager.transcribe(
            await file.read(), file.filename or "audio.wav", file.content_type or "audio/wav"
        )
    except SpeechRecognitionError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    return TranscriptionResponse(text=text, wake_word_detected=detected)


@router.post("/commands", response_model=CommandResponse)
async def voice_command(
    request: Request,
    file: UploadFile = File(...),
    conversation_id: str | None = None,
) -> CommandResponse:
    """Convert a recorded phrase to an assistant response without retaining its audio."""

    try:
        text, _ = await request.app.state.voice_manager.transcribe(
            await file.read(), file.filename or "audio.wav", file.content_type or "audio/wav"
        )
        if not text:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wake word not detected.")
        session_id, response = await request.app.state.orchestrator.respond(text, conversation_id)
    except SpeechRecognitionError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    except LLMProviderError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    return CommandResponse(conversation_id=session_id, response=response, provider=request.app.state.llm.name)


@router.post("/speech", response_class=Response)
async def speak(payload: SpeakRequest, request: Request) -> Response:
    try:
        audio = await request.app.state.voice_manager.speak(payload.text, payload.voice, payload.speed)
    except TextToSpeechError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    return Response(content=audio, media_type="audio/wav")
