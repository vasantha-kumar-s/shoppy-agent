"""
AgentCart — Pydantic Schemas for Admin Dashboard.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class AdminLoginRequest(BaseModel):
    """Admin sign-in request."""
    email: str
    password: str


class AdminLoginResponse(BaseModel):
    """Admin sign-in response."""
    access_token: str
    token_type: str = "bearer"
    role: str = "admin"
    name: str = "Store Admin"


class AdminProductCreate(BaseModel):
    """Create product request from Admin."""
    name: str
    brand: str
    category: str  # slug or name
    price: float = Field(gt=0)
    original_price: Optional[float] = None
    stock: int = Field(ge=0, default=0)
    status: Optional[str] = "active"
    description: Optional[str] = ""
    sku: Optional[str] = None
    image_url: Optional[str] = None
    specifications: Optional[dict[str, Any]] = None
    warranty: Optional[str] = None


class AdminProductUpdate(BaseModel):
    """Update product request from Admin."""
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    stock: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    image_url: Optional[str] = None
    specifications: Optional[dict[str, Any]] = None
    warranty: Optional[str] = None


class AdminStockUpdate(BaseModel):
    """Stock adjustment request."""
    stock: int = Field(ge=0)


class AdminOrderStatusUpdate(BaseModel):
    """Order status update."""
    status: str


class AdminCustomerOut(BaseModel):
    """Customer summary for admin."""
    id: int
    name: str
    email: str
    city: str
    orders: int
    spent: float
    joined: str


class AdminOrderOut(BaseModel):
    """Order summary for admin."""
    id: int
    order_number: str
    customer: str
    items: int
    total: float
    status: str
    date: str


class AdminAnalyticsOut(BaseModel):
    """Analytics overview for admin."""
    revenue: float
    orders: int
    avg_order_value: float
    cancellation_rate: str
    sales_by_month: list[list[Any]]
    sales_by_category: list[list[Any]]

