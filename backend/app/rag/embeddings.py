"""
AgentCart — Local Embeddings via Ollama.

Uses local Ollama embedding models (e.g. nomic-embed-text) with zero cloud API keys.
"""

import httpx
import logging
from typing import List
from app.core.config import settings

logger = logging.getLogger(__name__)


async def get_embedding(text: str) -> List[float]:
    """Generate a vector embedding using Ollama's local embedding endpoint."""
    url = f"{settings.OLLAMA_HOST}/api/embeddings"
    payload = {
        "model": settings.EMBEDDING_MODEL,
        "prompt": text,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("embedding", [])
            else:
                logger.warning(f"Ollama embeddings returned status {resp.status_code}")
    except Exception as e:
        logger.warning(f"Failed to generate embeddings via Ollama ({e}).")

    return []
