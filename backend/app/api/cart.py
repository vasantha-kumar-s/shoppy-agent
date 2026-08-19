"""
AgentCart — Cart API Endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_cart_service, get_current_user_id
from app.services.cart_service import CartService
from app.schemas.cart import CartItemCreate, CartItemUpdate

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.get("")
async def get_cart(
    user_id: int = Depends(get_current_user_id),
    service: CartService = Depends(get_cart_service),
):
    """Get current cart contents."""
    return await service.get_cart(user_id)


@router.post("/items")
async def add_to_cart(
    item: CartItemCreate,
    user_id: int = Depends(get_current_user_id),
    service: CartService = Depends(get_cart_service),
):
    """Add a product to cart."""
    result = await service.add_to_cart(user_id, item.product_id, item.quantity)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("/items/{product_id}")
async def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    user_id: int = Depends(get_current_user_id),
    service: CartService = Depends(get_cart_service),
):
    """Update quantity of a cart item."""
    result = await service.update_quantity(user_id, product_id, item.quantity)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("/items/{product_id}")
async def remove_from_cart(
    product_id: int,
    user_id: int = Depends(get_current_user_id),
    service: CartService = Depends(get_cart_service),
):
    """Remove a product from cart."""
    result = await service.remove_from_cart(user_id, product_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.delete("")
async def clear_cart(
    user_id: int = Depends(get_current_user_id),
    service: CartService = Depends(get_cart_service),
):
    """Clear all items from cart."""
    return await service.clear_cart(user_id)
