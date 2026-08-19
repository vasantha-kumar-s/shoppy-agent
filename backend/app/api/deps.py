"""
AgentCart — API Dependencies.

Shared FastAPI dependencies for database sessions and user resolution.
"""

from fastapi import Depends, Header
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.order_service import OrderService


async def get_product_service(
    db: AsyncSession = Depends(get_db),
) -> ProductService:
    """Dependency: ProductService instance."""
    return ProductService(db)


async def get_cart_service(
    db: AsyncSession = Depends(get_db),
) -> CartService:
    """Dependency: CartService instance."""
    return CartService(db)


async def get_order_service(
    db: AsyncSession = Depends(get_db),
) -> OrderService:
    """Dependency: OrderService instance."""
    return OrderService(db)


async def get_current_user_id(
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
) -> int:
    """
    Resolve current user ID from header.
    For this demo, defaults to user 1 if not provided.
    """
    if x_user_id:
        try:
            return int(x_user_id)
        except ValueError:
            pass
    return 1  # Demo user
