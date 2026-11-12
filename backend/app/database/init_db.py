"""
AgentCart — Database Initialization.

Creates all tables and enables pgvector extension when available.
"""

import logging
from sqlalchemy import text
from app.database.connection import engine
from app.database.base import Base

# Import all models to register them with Base.metadata
import app.models  # noqa: F401

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Create all tables and enable extensions."""
    # 1. Try enabling pgvector in isolated transaction
    try:
        async with engine.begin() as conn:
            avail = await conn.execute(
                text("SELECT 1 FROM pg_available_extensions WHERE name = 'vector'")
            )
            if avail.scalar():
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                logger.info("✅ pgvector extension enabled")
            else:
                logger.info("ℹ️ pgvector extension not present in PostgreSQL; running with text/keyword RAG fallback.")
    except Exception as e:
        logger.warning(f"Could not initialize pgvector extension: {e}. Falling back to keyword search.")

    # 2. Create all application tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ All database tables created")


async def drop_db() -> None:
    """Drop all tables (use with caution — for development only)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("All database tables dropped")
