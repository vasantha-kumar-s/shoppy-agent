"""
AgentCart — High-Efficiency Product Tools.
"""

from langchain_core.tools import tool
from typing import Optional, List
from app.database.connection import async_session_factory
from app.services.product_service import ProductService


@tool
async def search_products(
    query: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    limit: int = 3,
) -> dict:
    """Search catalog products by query, category, or max price in INR."""
    # Sanitize inputs from smaller LLMs
    if category and category.lower() in ["", "all", "none", "null", "any", "products", "items"]:
        category = None
    if query and query.lower() in ["", "all", "none", "null", "any", "products", "items", "all products", "all items"]:
        query = None

    async with async_session_factory() as session:
        service = ProductService(session)
        products = await service.search_products(
            query=query,
            category=category,
            max_price=max_price,
            limit=min(limit, 5),
        )

        if not products:
            return {"products": [], "message": "No matching products found."}

        return {
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "brand": p.brand,
                    "price": p.price,
                    "rating": p.rating,
                    "stock": p.inventory.quantity if p.inventory else 0,
                    "warranty": p.warranty,
                }
                for p in products
            ]
        }


@tool
async def get_product_details(product_id: int) -> dict:
    """Get full specs and stock for a product by ID."""
    async with async_session_factory() as session:
        service = ProductService(session)
        p = await service.get_product_by_id(product_id)
        if not p:
            return {"error": f"Product ID {product_id} not found."}
        return {
            "id": p.id,
            "name": p.name,
            "brand": p.brand,
            "price": p.price,
            "rating": p.rating,
            "stock": p.inventory.quantity if p.inventory else 0,
            "specifications": p.specifications or {},
            "description": p.description,
        }


@tool
async def compare_products(product_ids: List[int]) -> dict:
    """Compare 2 or more products by their IDs."""
    if len(product_ids) < 2:
        return {"error": "Need at least 2 product IDs."}
    async with async_session_factory() as session:
        service = ProductService(session)
        return await service.compare_products(product_ids)


@tool
async def check_stock(product_id: int, quantity: int = 1) -> dict:
    """Check inventory stock for a product ID."""
    async with async_session_factory() as session:
        service = ProductService(session)
        return await service.check_stock(product_id, quantity)
