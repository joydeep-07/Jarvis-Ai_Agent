import pytest


@pytest.mark.asyncio
async def test_orchestrator_retains_conversation(orchestrator):
    session_id, reply = await orchestrator.respond("Hello", "session-1")
    assert session_id == "session-1"
    assert reply == "Acknowledged: Hello"

    _, second_reply = await orchestrator.respond("Again", "session-1")
    assert second_reply == "Acknowledged: Again"
