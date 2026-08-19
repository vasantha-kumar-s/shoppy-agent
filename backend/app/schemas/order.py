"""
AgentCart — Pydantic Schemas for Orders.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderCreate(BaseModel):
    """Request to create a simulated order."""
    shipping_address_id: Optional[int] = None


class OrderItemOut(BaseModel):
    """Single item in an order."""
    id: int
    product_id: int
    product_name: str
    quantity: int
    price_at_purchase: float
    subtotal: float

    model_config = {"from_attributes": True}


class AddressOut(BaseModel):
    """Address in order response."""
    id: int
    label: str
    street: str
    city: str
    state: str
    pincode: str

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    """Full order response."""
    id: int
    order_number: str
    user_id: int
    status: str
    total_amount: float
    shipping_address: Optional[AddressOut] = None
    items: list[OrderItemOut]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class OrderSummary(BaseModel):
    """Compact order for list view."""
    id: int
    order_number: str
    status: str
    total_amount: float
    item_count: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
