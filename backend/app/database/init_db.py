"""
AgentCart — Database Initialization.

Creates all tables and enables pgvector extension.
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
    async with engine.begin() as conn:
        # Enable pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        logger.info("pgvector extension enabled")

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("All database tables created")


async def drop_db() -> None:
    """Drop all tables (use with caution — for development only)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("All database tables dropped")
