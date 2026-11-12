"""
AgentCart — Speech-to-Text Service.

Communicates with the self-hosted faster-whisper REST service.
"""

import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class STTService:
    """Service to transcribe audio files via faster-whisper REST container."""

    @staticmethod
    async def transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
        """Send audio bytes to faster-whisper endpoint and return transcribed text."""
        # 1. First try onerahmet/openai-whisper-asr-webservice (/asr with audio_file field)
        asr_url = f"{settings.WHISPER_URL}/asr"
        params = {
            "task": "transcribe",
            "language": "en",
            "output": "json",
            "encode": "true",
        }
        files_primary = {"audio_file": (filename, audio_bytes, "audio/webm")}

        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.post(asr_url, params=params, files=files_primary)
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        if isinstance(data, dict):
                            return (data.get("text") or "").strip()
                    except Exception:
                        pass
                    return resp.text.strip()
                logger.warning(f"Whisper /asr returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.warning(f"Whisper /asr failed: {e}")

        # 2. Fallback to standard OpenAI-compatible (/v1/audio/transcriptions with file field)
        v1_url = f"{settings.WHISPER_URL}/v1/audio/transcriptions"
        files_fallback = {"file": (filename, audio_bytes, "audio/webm")}
        data_fallback = {"model": settings.WHISPER_MODEL, "language": "en"}

        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.post(v1_url, files=files_fallback, data=data_fallback)
                if resp.status_code == 200:
                    json_data = resp.json()
                    return (json_data.get("text") or "").strip()
        except Exception as e:
            logger.warning(f"Whisper /v1/audio/transcriptions fallback failed: {e}")

        raise RuntimeError("Whisper STT service is unreachable or returned an error.")
