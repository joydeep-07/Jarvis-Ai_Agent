from app.memory.short_term import ShortTermMemory


class MemoryManager:
    """Facade that isolates callers from future long-term and semantic stores."""

    def __init__(self) -> None:
        self.short_term = ShortTermMemory()

    def conversation(self, conversation_id: str):
        return self.short_term.get(conversation_id)
