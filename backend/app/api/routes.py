from fastapi import APIRouter, HTTPException, Request, status

from app.ai.groq_client import LLMProviderError
from app.schemas.commands import CommandRequest, CommandResponse

router = APIRouter(prefix="/commands", tags=["commands"])


@router.post("", response_model=CommandResponse)
async def command(payload: CommandRequest, request: Request) -> CommandResponse:
    try:
        conversation_id, response = await request.app.state.orchestrator.respond(
            payload.message, payload.conversation_id
        )
    except LLMProviderError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    return CommandResponse(conversation_id=conversation_id, response=response, provider=request.app.state.llm.name)
