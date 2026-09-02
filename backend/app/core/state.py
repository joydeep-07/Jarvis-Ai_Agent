from enum import StrEnum


class AssistantState(StrEnum):
    IDLE = "IDLE"
    THINKING = "THINKING"
    ERROR = "ERROR"
