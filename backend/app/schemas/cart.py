"""
AgentCart — Pydantic Schemas for Cart.
"""

from pydantic import BaseModel, Field
from typing import Optional


class CartItemCreate(BaseModel):
    """Request to add item to cart."""
    product_id: int
    quantity: int = Field(1, ge=1)


class CartItemUpdate(BaseModel):
    """Request to update cart item quantity."""
    quantity: int = Field(ge=1)


class CartItemOut(BaseModel):
    """Cart item in response."""
    id: int
    product_id: int
    product_name: str
    product_brand: str
    product_price: float
    product_image_url: Optional[str] = None
    quantity: int
    subtotal: float

    model_config = {"from_attributes": True}


class CartOut(BaseModel):
    """Full cart response."""
    id: int
    user_id: int
    items: list[CartItemOut]
    total_items: int
    total_amount: float

    model_config = {"from_attributes": True}
