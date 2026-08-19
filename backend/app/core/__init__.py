"""
AgentCart — Application Configuration.

All settings loaded from environment variables with sensible defaults.
No paid API keys required.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Central configuration loaded from .env file."""

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://agentcart:agentcart_secret@localhost:5432/agentcart"

    # --- Ollama (LLM) ---
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"

    # --- Embeddings ---
    EMBEDDING_MODEL: str = "nomic-embed-text"

    # --- Voice: Speech-to-Text (faster-whisper) ---
    WHISPER_URL: str = "http://localhost:9000"
    WHISPER_MODEL: str = "base"

    # --- Voice: Text-to-Speech (Kokoro) ---
    KOKORO_URL: str = "http://localhost:8880"
    KOKORO_VOICE: str = "af_heart"

    # --- Backend ---
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Singleton settings instance
settings = Settings()
