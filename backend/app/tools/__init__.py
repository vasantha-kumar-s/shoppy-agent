"""
AgentCart — All Agent Tools Registry.
"""

from app.tools.product_tools import (
    search_products,
    get_product_details,
    compare_products,
    check_stock,
)
from app.tools.cart_tools import (
    get_cart,
    add_to_cart,
    remove_from_cart,
    clear_cart,
)
from app.tools.order_tools import (
    create_order,
    get_order_history,
)
from app.tools.rag_tools import search_policies

# High-efficiency toolset (compact schemas for sub-second local LLM parsing)
ALL_TOOLS = [
    search_products,
    get_product_details,
    compare_products,
    check_stock,
    get_cart,
    add_to_cart,
    remove_from_cart,
    clear_cart,
    create_order,
    get_order_history,
    search_policies,
]
