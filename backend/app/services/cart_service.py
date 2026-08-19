"""
AgentCart — Cart Service Layer.

All cart mutations go through this service.
"""

import logging
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.inventory import Inventory

logger = logging.getLogger(__name__)


class CartService:
    """Service for cart CRUD operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_cart(self, user_id: int) -> Cart:
        """Get existing cart or create a new one for the user."""
        stmt = (
            select(Cart)
            .options(selectinload(Cart.items).selectinload(CartItem.product))
            .where(Cart.user_id == user_id)
            .execution_options(populate_existing=True)
        )
        result = await self.db.execute(stmt)
        cart = result.scalars().first()

        if not cart:
            cart = Cart(user_id=user_id)
            self.db.add(cart)
            await self.db.flush()
            # Re-fetch with relationships loaded
            result = await self.db.execute(
                select(Cart)
                .options(selectinload(Cart.items).selectinload(CartItem.product))
                .where(Cart.id == cart.id)
                .execution_options(populate_existing=True)
            )
            cart = result.scalars().first()

        return cart

    async def get_cart(self, user_id: int) -> dict:
        """Get cart contents with computed totals."""
        cart = await self.get_or_create_cart(user_id)

        items = []
        total_amount = 0.0
        total_items = 0

        # Query items directly for absolute freshness
        items_stmt = (
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.cart_id == cart.id)
            .execution_options(populate_existing=True)
        )
        res = await self.db.execute(items_stmt)
        cart_items = list(res.scalars().all())

        for item in cart_items:
            product = item.product
            subtotal = product.price * item.quantity
            total_amount += subtotal
            total_items += item.quantity
            items.append({
                "id": item.id,
                "product_id": product.id,
                "product_name": product.name,
                "product_brand": product.brand,
                "product_price": product.price,
                "product_image_url": product.image_url,
                "quantity": item.quantity,
                "subtotal": round(subtotal, 2),
            })

        return {
            "id": cart.id,
            "user_id": user_id,
            "items": items,
            "total_items": total_items,
            "total_amount": round(total_amount, 2),
        }

    async def add_to_cart(
        self, user_id: int, product_id: int, quantity: int = 1
    ) -> dict:
        """Add a product to cart. If already in cart, increase quantity."""
        product = await self.db.get(Product, product_id)
        if not product:
            return {"error": f"Product ID {product_id} not found"}

        inv_result = await self.db.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        inventory = inv_result.scalars().first()
        if not inventory or inventory.quantity < quantity:
            available = inventory.quantity if inventory else 0
            return {
                "error": f"Insufficient stock for {product.name}. "
                         f"Available: {available}, Requested: {quantity}"
            }

        cart = await self.get_or_create_cart(user_id)

        # Check existing item directly from DB
        item_stmt = select(CartItem).where(
            CartItem.cart_id == cart.id, CartItem.product_id == product_id
        )
        item_res = await self.db.execute(item_stmt)
        existing_item = item_res.scalars().first()

        if existing_item:
            new_qty = existing_item.quantity + quantity
            if inventory.quantity < new_qty:
                return {
                    "error": f"Cannot add {quantity} more. "
                             f"Already {existing_item.quantity} in cart, "
                             f"only {inventory.quantity} in stock."
                }
            existing_item.quantity = new_qty
        else:
            new_item = CartItem(
                cart_id=cart.id, product_id=product_id, quantity=quantity
            )
            self.db.add(new_item)

        await self.db.flush()
        logger.info(f"Added product {product_id} x{quantity} to cart for user {user_id}")

        return {
            "success": True,
            "message": f"Added {product.name} (x{quantity}) to your cart.",
            "product_name": product.name,
            "quantity": quantity,
        }

    async def remove_from_cart(self, user_id: int, product_id: int) -> dict:
        """Remove a product from cart entirely."""
        cart = await self.get_or_create_cart(user_id)

        item_stmt = select(CartItem).where(
            CartItem.cart_id == cart.id, CartItem.product_id == product_id
        )
        item_res = await self.db.execute(item_stmt)
        item = item_res.scalars().first()

        if item:
            await self.db.delete(item)
            await self.db.flush()
            logger.info(f"Removed product {product_id} from cart for user {user_id}")
            return {
                "success": True,
                "message": "Removed product from your cart.",
            }

        return {"error": f"Product ID {product_id} is not in your cart."}

    async def update_quantity(
        self, user_id: int, product_id: int, quantity: int
    ) -> dict:
        """Update the quantity of a product in cart."""
        cart = await self.get_or_create_cart(user_id)

        item_stmt = select(CartItem).where(
            CartItem.cart_id == cart.id, CartItem.product_id == product_id
        )
        item_res = await self.db.execute(item_stmt)
        item = item_res.scalars().first()

        if item:
            inv_result = await self.db.execute(
                select(Inventory).where(Inventory.product_id == product_id)
            )
            inventory = inv_result.scalars().first()
            if not inventory or inventory.quantity < quantity:
                available = inventory.quantity if inventory else 0
                return {
                    "error": f"Cannot set quantity to {quantity}. "
                             f"Only {available} in stock."
                }
            item.quantity = quantity
            await self.db.flush()
            return {
                "success": True,
                "message": f"Updated quantity to {quantity}.",
            }

        return {"error": f"Product ID {product_id} is not in your cart."}

    async def clear_cart(self, user_id: int) -> dict:
        """Remove all items from cart."""
        cart = await self.get_or_create_cart(user_id)

        await self.db.execute(
            delete(CartItem).where(CartItem.cart_id == cart.id)
        )
        await self.db.flush()

        logger.info(f"Cleared cart for user {user_id}")
        return {"success": True, "message": "Your cart has been cleared."}
