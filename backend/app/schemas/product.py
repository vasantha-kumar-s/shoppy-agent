"""
AgentCart — Pydantic Schemas for Products.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryOut(BaseModel):
    """Category response."""
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None

    model_config = {"from_attributes": True}


class InventoryOut(BaseModel):
    """Inventory response (embedded in product)."""
    quantity: int
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProductOut(BaseModel):
    """Product response — full details."""
    id: int
    name: str
    description: str
    brand: str
    category_id: int
    price: float
    rating: float
    specifications: Optional[dict] = None
    image_url: Optional[str] = None
    warranty: Optional[str] = None
    created_at: Optional[datetime] = None
    category: Optional[CategoryOut] = None
    inventory: Optional[InventoryOut] = None

    model_config = {"from_attributes": True}


class ProductSummary(BaseModel):
    """Compact product representation for lists."""
    id: int
    name: str
    brand: str
    price: float
    rating: float
    category_id: int
    image_url: Optional[str] = None
    stock: Optional[int] = None  # Derived from inventory

    model_config = {"from_attributes": True}


class ProductSearchParams(BaseModel):
    """Query parameters for product search."""
    query: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    brand: Optional[str] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)


class ProductComparisonOut(BaseModel):
    """Comparison of multiple products."""
    products: list[ProductOut]
    comparison_fields: list[str]


class StockCheckOut(BaseModel):
    """Stock availability result."""
    product_id: int
    product_name: str
    requested_quantity: int
    available_quantity: int
    in_stock: bool
