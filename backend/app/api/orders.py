"""
AgentCart — Order API Endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_order_service, get_current_user_id
from app.services.order_service import OrderService
from app.schemas.order import OrderCreate

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("")
async def create_order(
    body: OrderCreate,
    user_id: int = Depends(get_current_user_id),
    service: OrderService = Depends(get_order_service),
):
    """Create a simulated order from the current cart."""
    result = await service.create_order(user_id, body.shipping_address_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("")
async def get_order_history(
    user_id: int = Depends(get_current_user_id),
    service: OrderService = Depends(get_order_service),
):
    """Get all past orders."""
    return await service.get_order_history(user_id)


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    service: OrderService = Depends(get_order_service),
):
    """Get details of a specific order."""
    result = await service.get_order_status(user_id, order_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
