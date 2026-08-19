"""
AgentCart — FastAPI Application Entry Point.

Main application with CORS, lifespan, and all route registrations.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.init_db import init_db
from app.api import health, products, cart, orders, chat, voice

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("🚀 Starting AgentCart backend...")
    await init_db()
    logger.info("✅ Database initialized")
    yield
    logger.info("👋 Shutting down AgentCart backend...")


app = FastAPI(
    title="AgentCart API",
    description="Multimodal Agentic AI E-commerce Shopping Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(chat.router)
app.include_router(voice.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "AgentCart API",
        "version": "1.0.0",
        "description": "Multimodal Agentic AI E-commerce Shopping Assistant",
        "docs": "/docs",
    }
