from dataclasses import dataclass, field


@dataclass
class Conversation:
    """In-memory conversation context with a bounded message history."""

    messages: list[dict[str, str]] = field(default_factory=list)
    max_messages: int = 20

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        self.messages[:] = self.messages[-self.max_messages :]

    def history(self) -> list[dict[str, str]]:
        return list(self.messages)
