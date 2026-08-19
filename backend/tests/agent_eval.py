"""
AgentCart — Agent Evaluation Benchmark Suite.

Contains 20+ realistic user queries across search, comparison, stock checking,
cart manipulation, order management, and policy RAG retrieval.
Validates intended tool mapping and expected system behavior.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EVALUATION_DATASET = [
    # --- Category 1: Product Search & Filtering (5 cases) ---
    {
        "id": 1,
        "category": "Search & Filter",
        "user_query": "I need wireless headphones under ₹5000.",
        "expected_tool": "search_products",
        "description": "Category + budget constraint query",
    },
    {
        "id": 2,
        "category": "Search & Filter",
        "user_query": "Show me laptops suitable for Python programming with 16GB RAM.",
        "expected_tool": "search_products",
        "description": "Specification & workload search",
    },
    {
        "id": 3,
        "category": "Search & Filter",
        "user_query": "What are your top-rated gaming monitors?",
        "expected_tool": "search_products",
        "description": "Category rating search",
    },
    {
        "id": 4,
        "category": "Search & Filter",
        "user_query": "Find Logitech mechanical keyboards.",
        "expected_tool": "search_products",
        "description": "Brand + feature search",
    },
    {
        "id": 5,
        "category": "Search & Filter",
        "user_query": "Do you have any smartwatches under ₹5,000?",
        "expected_tool": "search_products",
        "description": "Budget smartwatch search",
    },

    # --- Category 2: Product Details & Specs (3 cases) ---
    {
        "id": 6,
        "category": "Product Details",
        "user_query": "Tell me more about product ID 16.",
        "expected_tool": "get_product_details",
        "description": "Full product specification retrieval",
    },
    {
        "id": 7,
        "category": "Product Details",
        "user_query": "What is the battery life of the Sony WH-1000XM5?",
        "expected_tool": "get_product_details",
        "description": "Specific attribute inquiry",
    },
    {
        "id": 8,
        "category": "Product Details",
        "user_query": "What ports are available on the Dell UltraSharp U2723QE monitor?",
        "expected_tool": "get_product_details",
        "description": "Hardware interface inspection",
    },

    # --- Category 3: Product Comparison (3 cases) ---
    {
        "id": 9,
        "category": "Comparison",
        "user_query": "Compare the MacBook Air M3 and ProBook Ultra 14.",
        "expected_tool": "compare_products",
        "description": "Side-by-side laptop comparison",
    },
    {
        "id": 10,
        "category": "Comparison",
        "user_query": "Compare product 16 and product 17.",
        "expected_tool": "compare_products",
        "description": "ID-based comparison",
    },
    {
        "id": 11,
        "category": "Comparison",
        "user_query": "Which one is lighter between the Razer DeathAdder V3 and G Pro X Superlight 2?",
        "expected_tool": "compare_products",
        "description": "Weight attribute comparison",
    },

    # --- Category 4: Inventory & Stock (2 cases) ---
    {
        "id": 12,
        "category": "Inventory",
        "user_query": "Is product ID 1 in stock right now?",
        "expected_tool": "check_stock",
        "description": "Availability check",
    },
    {
        "id": 13,
        "category": "Inventory",
        "user_query": "Do you have 5 units of the OnePlus 12R available?",
        "expected_tool": "check_stock",
        "description": "Quantity-specific stock check",
    },

    # --- Category 5: Cart Management (4 cases) ---
    {
        "id": 14,
        "category": "Cart",
        "user_query": "Add product ID 8 to my cart.",
        "expected_tool": "add_to_cart",
        "description": "Cart addition",
    },
    {
        "id": 15,
        "category": "Cart",
        "user_query": "What items are currently in my cart and what is the total?",
        "expected_tool": "get_cart",
        "description": "Cart inspection",
    },
    {
        "id": 16,
        "category": "Cart",
        "user_query": "Remove product 8 from my cart.",
        "expected_tool": "remove_from_cart",
        "description": "Cart item deletion",
    },
    {
        "id": 17,
        "category": "Cart",
        "user_query": "Clear my entire shopping cart.",
        "expected_tool": "clear_cart",
        "description": "Cart reset",
    },

    # --- Category 6: Order Simulation (3 cases) ---
    {
        "id": 18,
        "category": "Orders",
        "user_query": "Place my simulated order for the items in my cart.",
        "expected_tool": "create_order",
        "description": "Order creation",
    },
    {
        "id": 19,
        "category": "Orders",
        "user_query": "What is the status of order number 1?",
        "expected_tool": "get_order_status",
        "description": "Order tracking",
    },
    {
        "id": 20,
        "category": "Orders",
        "user_query": "Show me my past order history.",
        "expected_tool": "get_order_history",
        "description": "Order history query",
    },

    # --- Category 7: Policy & Store Knowledge RAG (3 cases) ---
    {
        "id": 21,
        "category": "Policy RAG",
        "user_query": "Can I return a laptop after 10 days?",
        "expected_tool": "search_policies",
        "description": "Return policy check",
    },
    {
        "id": 22,
        "category": "Policy RAG",
        "user_query": "What is the delivery time for Bangalore?",
        "expected_tool": "search_policies",
        "description": "Shipping timeframe check",
    },
    {
        "id": 23,
        "category": "Policy RAG",
        "user_query": "What warranty is covered if my monitor has dead pixels?",
        "expected_tool": "search_policies",
        "description": "Warranty terms inquiry",
    },

    # --- Category 8: Non-tool Conversational (2 cases) ---
    {
        "id": 24,
        "category": "Chitchat",
        "user_query": "Hello! How can you help me today?",
        "expected_tool": None,
        "description": "Direct greeting without tool invocation",
    },
    {
        "id": 25,
        "category": "Chitchat",
        "user_query": "Thank you for the help!",
        "expected_tool": None,
        "description": "Closing courtesy without tool invocation",
    },
]


def run_evaluation_summary():
    """Print evaluation dataset summary."""
    print("=" * 60)
    print("  AgentCart Evaluation Benchmark (25 Scenarios)")
    print("=" * 60)
    print(f"Total Test Cases: {len(EVALUATION_DATASET)}")

    categories = {}
    for item in EVALUATION_DATASET:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in categories.items():
        print(f"  - {cat.ljust(22)}: {count} test cases")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation_summary()
