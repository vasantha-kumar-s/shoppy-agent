"""
AgentCart — Health Check API.

Reports status of all services: DB, Ollama, Whisper, Kokoro.
"""

import logging
from fastapi import APIRouter
import httpx

from app.core.config import settings
from app.database.connection import engine

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])


@router.get("/api/health")
async def health_check():
    """Check health of all services."""
    status = {
        "status": "ok",
        "services": {}
    }

    # --- Database ---
    try:
        async with engine.connect() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        status["services"]["database"] = {"status": "online"}
    except Exception as e:
        status["services"]["database"] = {"status": "offline", "error": str(e)}
        status["status"] = "degraded"

    # --- Ollama ---
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.OLLAMA_HOST}/api/tags")
            if resp.status_code == 200:
                models = [m["name"] for m in resp.json().get("models", [])]
                status["services"]["ollama"] = {
                    "status": "online",
                    "models": models,
                    "configured_model": settings.OLLAMA_MODEL,
                }
            else:
                status["services"]["ollama"] = {"status": "offline"}
                status["status"] = "degraded"
    except Exception:
        status["services"]["ollama"] = {"status": "offline"}
        status["status"] = "degraded"

    # --- Whisper (STT) ---
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.WHISPER_URL}/docs")
            status["services"]["whisper_stt"] = {
                "status": "online" if resp.status_code in (200, 307, 404) else "offline"
            }
    except Exception:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{settings.WHISPER_URL}/")
                status["services"]["whisper_stt"] = {
                    "status": "online" if resp.status_code in (200, 307, 404) else "offline"
                }
        except Exception:
            status["services"]["whisper_stt"] = {"status": "offline"}

    # --- Kokoro (TTS) ---
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.KOKORO_URL}/docs")
            status["services"]["kokoro_tts"] = {
                "status": "online" if resp.status_code in (200, 307, 404, 405) else "offline"
            }
    except Exception:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{settings.KOKORO_URL}/v1/audio/speech")
                status["services"]["kokoro_tts"] = {
                    "status": "online" if resp.status_code in (200, 405) else "offline"
                }
        except Exception:
            status["services"]["kokoro_tts"] = {"status": "offline"}

    return status
