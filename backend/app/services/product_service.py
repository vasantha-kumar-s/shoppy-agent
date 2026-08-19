"""
AgentCart — Product Service Layer.

All product queries go through this service.
The LLM never touches SQL directly — it calls tools that use this service.
"""

import logging
from typing import Optional
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.category import Category
from app.models.inventory import Inventory

logger = logging.getLogger(__name__)


class ProductService:
    """Service for product search, filtering, comparison, and stock checks."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        brand: Optional[str] = None,
        min_rating: Optional[float] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Product]:
        """Search products with multiple filters."""
        stmt = (
            select(Product)
            .options(selectinload(Product.category), selectinload(Product.inventory))
        )

        conditions = []

        # Text search: match name, description, or brand
        if query:
            search_term = f"%{query.lower()}%"
            conditions.append(
                or_(
                    func.lower(Product.name).like(search_term),
                    func.lower(Product.description).like(search_term),
                    func.lower(Product.brand).like(search_term),
                )
            )

        # Category filter (match by slug or name)
        if category:
            cat_term = category.lower()
            stmt = stmt.join(Product.category)
            conditions.append(
                or_(
                    func.lower(Category.slug).like(f"%{cat_term}%"),
                    func.lower(Category.name).like(f"%{cat_term}%"),
                )
            )

        # Price range
        if min_price is not None:
            conditions.append(Product.price >= min_price)
        if max_price is not None:
            conditions.append(Product.price <= max_price)

        # Brand filter
        if brand:
            conditions.append(func.lower(Product.brand).like(f"%{brand.lower()}%"))

        # Rating filter
        if min_rating is not None:
            conditions.append(Product.rating >= min_rating)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(Product.rating.desc()).offset(offset).limit(limit)

        result = await self.db.execute(stmt)
        products = result.scalars().unique().all()

        # If strict text search returned 0 results but a category was specified, fallback to category search
        if not products and category and query:
            return await self.search_products(
                query=None,
                category=category,
                min_price=min_price,
                max_price=max_price,
                brand=brand,
                min_rating=min_rating,
                limit=limit,
                offset=offset,
            )

        logger.info(f"Product search returned {len(products)} results")
        return list(products)

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get full product details by ID."""
        stmt = (
            select(Product)
            .options(selectinload(Product.category), selectinload(Product.inventory))
            .where(Product.id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_products_by_ids(self, product_ids: list[int]) -> list[Product]:
        """Get multiple products by their IDs."""
        stmt = (
            select(Product)
            .options(selectinload(Product.category), selectinload(Product.inventory))
            .where(Product.id.in_(product_ids))
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().unique().all())

    async def filter_products(
        self, product_ids: list[int], criteria: dict
    ) -> list[Product]:
        """Filter a specific set of products by criteria."""
        products = await self.get_products_by_ids(product_ids)

        filtered = []
        for p in products:
            match = True
            if "min_price" in criteria and p.price < criteria["min_price"]:
                match = False
            if "max_price" in criteria and p.price > criteria["max_price"]:
                match = False
            if "brand" in criteria and criteria["brand"].lower() not in p.brand.lower():
                match = False
            if "min_rating" in criteria and p.rating < criteria["min_rating"]:
                match = False
            # Check specifications
            if "specs" in criteria and p.specifications:
                for key, value in criteria["specs"].items():
                    spec_val = p.specifications.get(key, "")
                    if isinstance(spec_val, str) and isinstance(value, str):
                        if value.lower() not in spec_val.lower():
                            match = False
            if match:
                filtered.append(p)

        return filtered

    async def compare_products(self, product_ids: list[int]) -> dict:
        """Create a structured comparison of products."""
        products = await self.get_products_by_ids(product_ids)

        if len(products) < 2:
            return {"error": "Need at least 2 products to compare", "products": []}

        # Collect all specification keys
        all_spec_keys = set()
        for p in products:
            if p.specifications:
                all_spec_keys.update(p.specifications.keys())

        comparison = {
            "products": [],
            "comparison_fields": sorted(all_spec_keys),
        }

        for p in products:
            product_data = {
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "price": p.price,
                "rating": p.rating,
                "warranty": p.warranty,
                "stock": p.inventory.quantity if p.inventory else 0,
                "specifications": {},
            }
            for key in sorted(all_spec_keys):
                product_data["specifications"][key] = (
                    p.specifications.get(key, "N/A") if p.specifications else "N/A"
                )
            comparison["products"].append(product_data)

        return comparison

    async def check_stock(self, product_id: int, quantity: int = 1) -> dict:
        """Check if a product has sufficient stock."""
        product = await self.get_product_by_id(product_id)
        if not product:
            return {
                "product_id": product_id,
                "product_name": "Unknown",
                "requested_quantity": quantity,
                "available_quantity": 0,
                "in_stock": False,
                "error": f"Product ID {product_id} not found",
            }

        available = product.inventory.quantity if product.inventory else 0
        return {
            "product_id": product_id,
            "product_name": product.name,
            "requested_quantity": quantity,
            "available_quantity": available,
            "in_stock": available >= quantity,
        }

    async def get_all_categories(self) -> list[Category]:
        """Get all categories."""
        result = await self.db.execute(select(Category).order_by(Category.name))
        return list(result.scalars().all())
