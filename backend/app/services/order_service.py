"""
AgentCart — Order Service Layer.

Handles simulated order creation and status tracking.
"""

import logging
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.models.address import Address
from app.models.inventory import Inventory

logger = logging.getLogger(__name__)


class OrderService:
    """Service for simulated order operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(
        self, user_id: int, shipping_address_id: Optional[int] = None
    ) -> dict:
        """Create a simulated order from the user's cart."""

        # Get cart
        cart_res = await self.db.execute(select(Cart).where(Cart.user_id == user_id))
        cart = cart_res.scalars().first()

        if not cart:
            return {"error": "Your cart is empty. Add items before placing an order."}

        # Query cart items directly
        items_res = await self.db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.cart_id == cart.id)
        )
        cart_items = list(items_res.scalars().all())

        if not cart_items:
            return {"error": "Your cart is empty. Add items before placing an order."}

        # Resolve shipping address
        if shipping_address_id:
            address = await self.db.get(Address, shipping_address_id)
            if not address or address.user_id != user_id:
                return {"error": f"Address ID {shipping_address_id} not found."}
        else:
            # Use default address
            addr_result = await self.db.execute(
                select(Address)
                .where(Address.user_id == user_id, Address.is_default == True)
            )
            address = addr_result.scalars().first()
            if not address:
                addr_result = await self.db.execute(
                    select(Address).where(Address.user_id == user_id).limit(1)
                )
                address = addr_result.scalars().first()

        # Calculate total and create order
        total_amount = 0.0
        order_items_data = []

        for item in cart_items:
            subtotal = item.product.price * item.quantity
            total_amount += subtotal
            order_items_data.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_purchase": item.product.price,
                "product_name": item.product.name,
            })

        # Create order
        order = Order(
            user_id=user_id,
            status="confirmed",
            total_amount=round(total_amount, 2),
            shipping_address_id=address.id if address else None,
        )
        self.db.add(order)
        await self.db.flush()

        # Create order items and reduce inventory
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price_at_purchase=item_data["price_at_purchase"],
            )
            self.db.add(order_item)

            # Reduce inventory
            inv_result = await self.db.execute(
                select(Inventory).where(Inventory.product_id == item_data["product_id"])
            )
            inventory = inv_result.scalars().first()
            if inventory:
                inventory.quantity = max(0, inventory.quantity - item_data["quantity"])

        # Clear cart items directly
        await self.db.execute(
            delete(CartItem).where(CartItem.cart_id == cart.id)
        )
        await self.db.flush()

        logger.info(f"Created order {order.order_number} for user {user_id}")

        return {
            "success": True,
            "id": order.id,
            "order_id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total_amount": order.total_amount,
            "items": [
                {
                    "product_name": d["product_name"],
                    "quantity": d["quantity"],
                    "price": d["price_at_purchase"],
                }
                for d in order_items_data
            ],
            "shipping_address": (
                f"{address.street}, {address.city}, {address.state} - {address.pincode}"
                if address else "No address provided"
            ),
            "message": f"Order {order.order_number} has been placed successfully! "
                       f"This is a simulated order — no real payment was charged.",
        }

    async def get_order_status(self, user_id: int, order_id: int) -> dict:
        """Get the status of a specific order."""
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.shipping_address),
            )
            .where(Order.id == order_id, Order.user_id == user_id)
        )
        order = result.scalars().first()

        if not order:
            return {"error": f"Order ID {order_id} not found."}

        return self._order_to_dict(order)

    async def get_order_history(self, user_id: int) -> list[dict]:
        """Get all orders for a user."""
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.shipping_address),
            )
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        orders = result.scalars().unique().all()
        return [self._order_to_dict(o) for o in orders]

    def _order_to_dict(self, order: Order) -> dict:
        """Convert order to a dictionary response."""
        items = []
        for item in order.items:
            items.append({
                "product_id": item.product_id,
                "product_name": item.product.name if item.product else "Unknown",
                "quantity": item.quantity,
                "price_at_purchase": item.price_at_purchase,
                "subtotal": round(item.price_at_purchase * item.quantity, 2),
            })

        address_str = None
        if order.shipping_address:
            a = order.shipping_address
            address_str = f"{a.street}, {a.city}, {a.state} - {a.pincode}"

        return {
            "id": order.id,
            "order_id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total_amount": order.total_amount,
            "items": items,
            "item_count": len(items),
            "shipping_address": address_str,
            "created_at": order.created_at.isoformat() if order.created_at else None,
        }
