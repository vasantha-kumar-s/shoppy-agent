"""
AgentCart — Product API Endpoints.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional

from app.api.deps import get_product_service
from app.services.product_service import ProductService
from app.schemas.product import ProductOut, ProductSummary, StockCheckOut

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=list[ProductOut])
async def list_products(
    query: Optional[str] = Query(None, description="Search text"),
    category: Optional[str] = Query(None, description="Category slug or name"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    brand: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ProductService = Depends(get_product_service),
):
    """Search and filter products."""
    products = await service.search_products(
        query=query,
        category=category,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        min_rating=min_rating,
        limit=limit,
        offset=offset,
    )
    return products


@router.get("/categories")
async def list_categories(
    service: ProductService = Depends(get_product_service),
):
    """Get all product categories."""
    categories = await service.get_all_categories()
    return categories


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Get full product details."""
    product = await service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@router.post("/compare")
async def compare_products(
    product_ids: list[int],
    service: ProductService = Depends(get_product_service),
):
    """Compare multiple products side by side."""
    if len(product_ids) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 products to compare")
    if len(product_ids) > 5:
        raise HTTPException(status_code=400, detail="Can compare at most 5 products")

    result = await service.compare_products(product_ids)
    return result


@router.get("/{product_id}/stock")
async def check_stock(
    product_id: int,
    quantity: int = Query(1, ge=1),
    service: ProductService = Depends(get_product_service),
):
    """Check stock availability for a product."""
    result = await service.check_stock(product_id, quantity)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
