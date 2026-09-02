"""Centralized, environment-based application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings. Values can be supplied through ``backend/.env``."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Jarvis"
    debug: bool = False
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///../data/jarvis.db"
    groq_api_key: str | None = Field(default=None, repr=False)
    groq_model: str = "llama-3.3-70b-versatile"
    groq_stt_model: str = "whisper-large-v3-turbo"
    groq_tts_model: str = "canopylabs/orpheus-v1-english"
    groq_timeout_seconds: float = 30.0
    max_agent_iterations: int = 6
    voice_enabled: bool = False
    wake_word_enabled: bool = False
    data_dir: Path = Path("../data")


@lru_cache
def get_settings() -> Settings:
    """Return the single immutable settings instance used by the application."""

    return Settings()
