"""
AgentCart — SQLAlchemy ORM Models.

All 13 database tables for the e-commerce platform.
"""

from app.database.base import Base
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.address import Address
from app.models.conversation import Conversation, Message
from app.models.document import Document
from app.models.review import ProductReview

# Re-export all models so Alembic and init_db can discover them
__all__ = [
    "Base",
    "User",
    "Category",
    "Product",
    "Inventory",
    "Cart",
    "CartItem",
    "Order",
    "OrderItem",
    "Address",
    "Conversation",
    "Message",
    "Document",
    "ProductReview",
]
