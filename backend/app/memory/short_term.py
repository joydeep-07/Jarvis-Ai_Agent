from app.ai.conversation import Conversation


class ShortTermMemory:
    """Conversation sessions, intentionally kept in memory in Phase 1."""

    def __init__(self) -> None:
        self._sessions: dict[str, Conversation] = {}

    def get(self, conversation_id: str) -> Conversation:
        return self._sessions.setdefault(conversation_id, Conversation())
