"""
AgentCart — High-Efficiency Order Tools.
"""

from langchain_core.tools import tool
from typing import Optional
from app.database.connection import async_session_factory
from app.services.order_service import OrderService


@tool
async def create_order(user_id: int = 1) -> dict:
    """Place a simulated checkout order for current items in the user's cart."""
    async with async_session_factory() as session:
        service = OrderService(session)
        res = await service.create_order(user_id)
        await session.commit()
        return res


@tool
async def get_order_history(user_id: int = 1) -> dict:
    """Get the user's past simulated orders."""
    async with async_session_factory() as session:
        service = OrderService(session)
        orders = await service.get_order_history(user_id)
        return {"orders": orders}
