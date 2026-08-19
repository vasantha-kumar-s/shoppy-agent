"""
AgentCart — High-Efficiency Cart Tools.
"""

from langchain_core.tools import tool
from app.database.connection import async_session_factory
from app.services.cart_service import CartService


@tool
async def get_cart(user_id: int = 1) -> dict:
    """Get items, quantities, and total amount in the user's cart."""
    async with async_session_factory() as session:
        service = CartService(session)
        return await service.get_cart(user_id)


@tool
async def add_to_cart(product_id: int, quantity: int = 1, user_id: int = 1) -> dict:
    """Add a product ID and quantity to the user's cart."""
    async with async_session_factory() as session:
        service = CartService(session)
        res = await service.add_to_cart(user_id, product_id, quantity)
        await session.commit()
        return res


@tool
async def remove_from_cart(product_id: int, user_id: int = 1) -> dict:
    """Remove a product ID from the user's cart."""
    async with async_session_factory() as session:
        service = CartService(session)
        res = await service.remove_from_cart(user_id, product_id)
        await session.commit()
        return res


@tool
async def clear_cart(user_id: int = 1) -> dict:
    """Clear all items from the user's cart."""
    async with async_session_factory() as session:
        service = CartService(session)
        res = await service.clear_cart(user_id)
        await session.commit()
        return res
