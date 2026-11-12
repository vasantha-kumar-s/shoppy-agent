"""
AgentCart — Text-to-Speech Service.

Communicates with the self-hosted Kokoro-FastAPI TTS container.
"""

import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class TTSService:
    """Service to synthesize speech from text using Kokoro-FastAPI."""

    @staticmethod
    async def synthesize(text: str) -> bytes:
        """Send text to Kokoro /v1/audio/speech endpoint and return audio bytes."""
        url = f"{settings.KOKORO_URL}/v1/audio/speech"
        payload = {
            "model": "kokoro",
            "input": text,
            "voice": settings.KOKORO_VOICE,
            "response_format": "mp3",
        }

        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    return resp.content
                else:
                    logger.warning(f"Kokoro TTS returned status {resp.status_code}")
        except Exception as e:
            logger.warning(f"Kokoro TTS connection error: {e}")

        raise RuntimeError("Kokoro TTS service is unreachable.")
