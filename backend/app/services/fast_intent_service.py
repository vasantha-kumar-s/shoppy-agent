"""
AgentCart — Context-Aware Fast Intent & Catalog Matcher Service.

Provides instant (<100ms) execution for all core e-commerce shopping requests:
- Show all products / Browse catalog
- Product search & filtering
- Stock availability checks
- Contextual Add-to-Cart (with typo tolerance: card/cart/bag/basket/it/this)
- View Cart (handles "show me the card", "show my cart", "cart", etc.)
- Real Database Order History & Order Status
- Affirmative Checkout & Order Placement ("yes", "place order", "confirm")
- Accurate Store Policy FAQs (Return, Shipping, Warranty, Payment)
- Warm Conversational Responses (Greetings, Reactions, Politeness)
"""

import re
import logging
from typing import Optional, Dict, Any, List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.services.memory_service import MemoryService
from app.models.document import Document

logger = logging.getLogger(__name__)


class FastIntentService:
    """Intelligent context-aware rule-based matcher for instant e-commerce responses."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_service = ProductService(session)
        self.cart_service = CartService(session)
        self.order_service = OrderService(session)
        self.memory_service = MemoryService(session)

    async def try_resolve_intent(
        self, text: str, user_id: int = 1, conversation_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Attempt to resolve user shopping request instantly. Returns response dict if handled, else None."""
        raw_clean = re.sub(r'[?.!,;:]+$', '', text.lower().strip()).strip()

        # -------------------------------------------------------------
        # 1. Polite Greetings & Common Reactions
        # -------------------------------------------------------------
        if re.match(r"^(h[ie]+y*|hello+|greetings|howdy|sup|good\s+(morning|afternoon|evening)|yo+)(?:\s+(there|assistant|shoppy|bot))?$", raw_clean):
            return {
                "response": "Hello! I'm your AgentCart shopping assistant. How can I help you today? You can search for products (e.g. 'find laptops under ₹70,000'), check stock, or manage your cart.",
                "products": [],
                "tool_activities": [],
            }

        if raw_clean in ["who are you", "what can you do", "help", "help me", "what is this", "what do you do"]:
            return {
                "response": "I'm your AgentCart AI shopping assistant! I can help you discover products, compare features side-by-side, check real-time stock, manage your cart, and place simulated orders. Try asking: 'Find wireless headphones under 5k' or 'What is the return policy?'",
                "products": [],
                "tool_activities": [],
            }

        # Remove leading conversational prefixes only if followed by additional words
        clean = re.sub(r'^[,\s]*(so|well|hey|hi|hello|ok|okay)[,\s]+', '', raw_clean).strip()
        clean = re.sub(r'[?.!,;:]+$', '', clean).strip()

        if clean in ["my god", "omg", "wow", "nice", "cool", "super", "great", "awesome", "perfect"]:
            return {
                "response": "I'm glad to assist you! 😊 How can I help next? You can check out your cart, search for products, or track an order.",
                "products": [],
                "tool_activities": [],
            }


        # -------------------------------------------------------------
        # 1.5 Product Comparison Intent ("compare google and samsung", "google and samsung", "compare pixel 8a vs galaxy s24")
        # -------------------------------------------------------------
        comp_m = re.search(r'\b(?:compare\s+)?([a-zA-Z0-9\s]+?)\s+(?:and|vs|with)\s+([a-zA-Z0-9\s]+)\b', clean)
        is_comp_q = "compare" in clean or (" vs " in clean) or (comp_m and any(b in clean for b in ["google", "samsung", "apple", "hp", "asus", "lenovo", "acer", "sony", "dell", "oneplus", "boat"]))
        if is_comp_q and comp_m:
            term1 = comp_m.group(1).replace("compare", "").strip()
            term2 = comp_m.group(2).strip()
            if term1 and term2 and len(term1) >= 2 and len(term2) >= 2:
                prods1 = await self.product_service.search_products(query=term1, limit=1)
                prods2 = await self.product_service.search_products(query=term2, limit=1)
                if prods1 and prods2 and prods1[0].id != prods2[0].id:
                    p1 = prods1[0]
                    p2 = prods2[0]
                    lines = [f"Here is the side-by-side comparison between **{p1.name}** and **{p2.name}**:\n"]
                    lines.append(f"### {p1.name} ({p1.brand})")
                    lines.append(f"• **Price:** ₹{p1.price:,.0f} | **Rating:** ⭐ {p1.rating} | **Stock:** {p1.inventory.quantity if p1.inventory else 0} units")
                    lines.append(f"• **Warranty:** {p1.warranty or '1 Year'}")
                    if p1.specifications:
                        for k, v in p1.specifications.items():
                            lines.append(f"• **{k.capitalize()}:** {v}")
                    lines.append(f"\n### {p2.name} ({p2.brand})")
                    lines.append(f"• **Price:** ₹{p2.price:,.0f} | **Rating:** ⭐ {p2.rating} | **Stock:** {p2.inventory.quantity if p2.inventory else 0} units")
                    lines.append(f"• **Warranty:** {p2.warranty or '1 Year'}")
                    if p2.specifications:
                        for k, v in p2.specifications.items():
                            lines.append(f"• **{k.capitalize()}:** {v}")
                    lines.append("\nBoth devices are available! Would you like full specifications or to add one to your cart?")
                    return {
                        "response": "\n".join(lines),
                        "products": [self._format_prod(p1), self._format_prod(p2)],
                        "tool_activities": [
                            {"tool_name": "compare_products", "status": "completed", "display_text": f"Comparing {p1.name} vs {p2.name}"}
                        ]
                    }

        if clean in ["thanks", "thank you", "thx", "thank you so much", "appreciate it"]:
            return {
                "response": "You're very welcome! Feel free to ask if you need anything else for your shopping.",
                "products": [],
                "tool_activities": [],
            }

        # -------------------------------------------------------------
        # 2. Affirmative Checkout & Order Placement ("yes", "place order", "proceed", "checkout")
        # -------------------------------------------------------------
        if (
            clean in ["yes", "yeah", "yep", "sure", "proceed", "confirm", "confirm order", "go ahead", "do it", "place it", "buy"]
            or any(p in clean for p in ["place order", "place the order", "place my order", "checkout", "buy now", "complete order", "check out"])
        ):
            cart_data = await self.cart_service.get_cart(user_id)
            items = cart_data.get("items", [])
            if not items:
                return {
                    "response": "Your shopping cart is currently empty! Please add some products to your cart before placing an order.",
                    "products": [],
                    "tool_activities": [],
                }

            res = await self.order_service.create_order(user_id)
            await self.session.commit()
            return {
                "response": (
                    f"🎉 **Order Placed Successfully!**\n\n"
                    f"• Order Number: **#{res['order_number']}**\n"
                    f"• Total Paid: **₹{res['total_amount']:,.0f}**\n"
                    f"• Status: **Confirmed**\n"
                    f"• Estimated Delivery: **2–4 Business Days**\n\n"
                    f"Your cart has been checked out. You can track this anytime under the **Orders** tab!"
                ),
                "products": [],
                "tool_activities": [
                    {"tool_name": "create_order", "status": "completed", "display_text": f"Created Order #{res['order_number']}"}
                ],
            }

        # -------------------------------------------------------------
        # 3. View Cart Intent (Handles "show me the card", "show my cart", "cart", "view card", etc.)
        # -------------------------------------------------------------
        if (
            re.search(r'\b(show|view|open|see|check|display|inspect|what is in|whats in|items in)\b.*\b(cart|card|kart|bag|basket)\b', clean)
            or clean in ["cart", "card", "kart", "my cart", "my card", "the cart", "the card", "show cart", "show card", "show my cart", "show my card", "view cart", "view card", "view my cart", "view my card", "check cart", "check card", "open cart", "open card", "bag", "my bag"]
            or any(p in clean for p in ["in my cart", "in my card", "in the cart", "in the card", "products in cart", "products in card", "cart contents", "card contents"])
        ):
            cart_data = await self.cart_service.get_cart(user_id)
            items = cart_data.get("items", [])
            if not items:
                return {
                    "response": "Your shopping cart is currently empty. Would you like some product recommendations?",
                    "products": [],
                    "tool_activities": [
                        {"tool_name": "get_cart", "status": "completed", "display_text": "Inspected shopping cart"}
                    ],
                }
            items_str = "\n".join([
                f"• **{i['product_name']}** — {i['quantity']}× @ ₹{i['product_price']:,.0f} (Subtotal: ₹{i['subtotal']:,.0f})"
                for i in items
            ])
            return {
                "response": (
                    f"Here are the items in your cart:\n\n{items_str}\n\n"
                    f"**Total ({cart_data['total_items']} items): ₹{cart_data['total_amount']:,.0f}**\n\n"
                    f"Ready to place your simulated order? (Say *\"Yes\"* or *\"Place order\"* to proceed)"
                ),
                "products": [],
                "tool_activities": [
                    {"tool_name": "get_cart", "status": "completed", "display_text": f"Loaded {len(items)} cart items"}
                ],
            }

        # -------------------------------------------------------------
        # 4. Real Database Order History ("order history", "my orders", "past orders", "track order")
        # -------------------------------------------------------------
        if any(p in clean for p in ["order history", "my orders", "past orders", "previous orders", "track order", "show orders", "list orders", "orders list"]):
            orders = await self.order_service.get_order_history(user_id)
            if not orders:
                return {
                    "response": "You haven't placed any orders yet! Once you checkout items from your cart, your order tracking and history will appear here.",
                    "products": [],
                    "tool_activities": [
                        {"tool_name": "get_order_history", "status": "completed", "display_text": "Retrieved order history"}
                    ],
                }

            order_bullets = []
            for o in orders[:5]:
                items_summary = ", ".join([f"{item['product_name']} (x{item['quantity']})" for item in o.get("items", [])[:2]])
                order_bullets.append(
                    f"• **Order #{o['order_number']}** — **₹{o['total_amount']:,.0f}**\n"
                    f"  Status: **{o['status'].title()}** | Items: {items_summary or 'Standard Order'}"
                )

            return {
                "response": "Here is your recent order history from the database:\n\n" + "\n\n".join(order_bullets) + "\n\nWould you like more details on any specific order?",
                "products": [],
                "tool_activities": [
                    {"tool_name": "get_order_history", "status": "completed", "display_text": f"Loaded {len(orders)} past orders"}
                ],
            }

        # -------------------------------------------------------------
        # 5. Show All Products / Browse Catalog Intent ("Show me all the items in the products", "show all products")
        # -------------------------------------------------------------
        if (
            any(p in clean for p in ["all products", "all the products", "all items", "all the items", "all items in the products", "browse products", "show catalog", "list products", "everything in store", "what do you have", "show all"])
            or clean in ["products", "items", "show products", "show items", "browse", "catalog"]
        ):
            featured_prods = await self.product_service.search_products(limit=4)
            prod_bullets = "\n\n".join([
                f"• **{p.name}** ({p.brand})\n  ₹{p.price:,.0f} | ⭐ {p.rating:.1f} | Stock: {p.inventory.quantity if p.inventory else 0} units | Warranty: {p.warranty}"
                for p in featured_prods
            ])
            return {
                "response": f"Here are some top-rated products from our catalog:\n\n{prod_bullets}\n\nWe have Laptops, Smartphones, Headphones, Monitors, Keyboards, Mice, and Smartwatches. Which category would you like to explore?",
                "products": [self._format_prod(p) for p in featured_prods],
                "tool_activities": [
                    {"tool_name": "search_products", "status": "completed", "display_text": f"Loaded {len(featured_prods)} catalog products"}
                ],
            }

        # -------------------------------------------------------------
        # 6. Add to Cart Intent ("Add Galaxy Buds to the card", "add to cart", "buy this")
        # -------------------------------------------------------------
        if (
            re.search(r'\b(add|put|buy|insert|include)\b.*\b(cart|card|kart|bag|basket)\b', clean)
            or clean.startswith("add ")
            or clean.startswith("buy ")
            or clean in ["add it", "add to cart", "add to card", "buy this", "buy it", "add this"]
        ):
            qty_match = re.search(r'\b(\d+)\s*(item|unit|piece|x)?\b', clean)
            qty = int(qty_match.group(1)) if qty_match and int(qty_match.group(1)) < 20 else 1

            term = re.sub(
                r'\b(add|put|buy|insert|include|to|my|the|in|into|cart|card|kart|bag|basket|please|item|product|unit|units|one|it|this|can you|just)\b',
                '',
                clean,
            )
            term = re.sub(r'[^a-zA-Z0-9\s]', '', term).strip()

            target_product = None

            # A. Search by extracted product keywords
            if term and len(term) >= 2:
                products = await self.product_service.search_products(query=term, limit=1)
                if not products and len(term.split()) > 1:
                    for w in term.split():
                        if len(w) >= 3:
                            prods = await self.product_service.search_products(query=w, limit=1)
                            if prods:
                                products = prods
                                break
                if products:
                    target_product = products[0]

            # B. Contextual Memory: search recent products mentioned in conversation
            if not target_product and conversation_id:
                recent_msgs = await self.memory_service.get_conversation_messages(conversation_id, limit=4)
                for msg in reversed(recent_msgs):
                    if msg.content:
                        bold_names = re.findall(r'\*\*([^*]+)\*\*', msg.content)
                        for b_name in bold_names:
                            prods = await self.product_service.search_products(query=b_name.strip(), limit=1)
                            if prods:
                                target_product = prods[0]
                                break
                    if target_product:
                        break

            if target_product:
                res = await self.cart_service.add_to_cart(user_id, target_product.id, qty)
                await self.session.commit()
                cart_info = await self.cart_service.get_cart(user_id)
                total_val = cart_info.get('total_amount', target_product.price * qty)
                return {
                    "response": (
                        f"Added **{qty}× {target_product.name}** ({target_product.brand}) to your cart! "
                        f"Total cart value is now **₹{total_val:,.0f}**.\n\n"
                        f"Would you like to view your cart or proceed to checkout?"
                    ),
                    "products": [self._format_prod(target_product)],
                    "tool_activities": [
                        {"tool_name": "add_to_cart", "status": "completed", "display_text": f"Added {target_product.name} to cart"}
                    ],
                }

        # -------------------------------------------------------------
        # 7. Check Stock / Availability Intent ("is tough gaming f15 available", "check stock of product 2")
        # -------------------------------------------------------------
        if any(w in clean for w in ["available", "in stock", "stock", "availability", "how many"]):
            term = re.sub(r'^(is|are|check|the|can i get|what is the stock of|how many)\s+', '', clean)
            term = re.sub(r'\s+(available|in stock|left|ready|to buy)\??$', '', term).strip()

            products = await self.product_service.search_products(query=term if len(term) > 2 else None, limit=3)
            if not products and len(term) > 3:
                words = [w for w in term.split() if len(w) > 3 and w not in ["laptop", "phone", "with", "gaming", "price"]]
                if words:
                    products = await self.product_service.search_products(query=words[0], limit=3)

            if products:
                p = products[0]
                qty = p.inventory.quantity if p.inventory else 0
                stock_status = f"**In Stock** ({qty} units ready to ship)" if qty > 0 else "**Out of Stock**"

                msg = (
                    f"Yes! The **{p.name}** by {p.brand} is currently {stock_status} at **₹{p.price:,.0f}**.\n\n"
                    f"• ⭐ Rating: {p.rating:.1f} / 5.0\n"
                    f"• 🛡️ Warranty: {p.warranty}\n\n"
                    f"Would you like me to add this to your shopping cart?"
                )
                return {
                    "response": msg,
                    "products": [self._format_prod(p) for p in products],
                    "tool_activities": [
                        {"tool_name": "check_stock", "status": "completed", "display_text": f"Checked stock for {p.name}"}
                    ],
                }

        # -------------------------------------------------------------
        # 8. Search & Filter Products ("show wireless headphones under 5k", "find laptops under 70000", "show mobiles")
        # -------------------------------------------------------------
        cat_match = None
        category_patterns = [
            (r'\b(?:smartphones?|mobiles?|cellphones?)\b', 'smartphones'),
            (r'\b(?:headphones?|earphones?|earbuds?|headsets?)\b', 'headphones'),
            (r'\b(?:laptops?|notebooks?|macbooks?)\b', 'laptops'),
            (r'\b(?:monitors?|screens?|displays?)\b', 'monitors'),
            (r'\b(?:keyboards?)\b', 'keyboards'),
            (r'\b(?:mice|mouse)\b', 'mice'),
            (r'\b(?:smartwatch(?:es)?|watches?)\b', 'smartwatches'),
            (r'\b(?:phones?)\b', 'smartphones'),
        ]
        for pat, cat_name in category_patterns:
            if re.search(pat, clean):
                cat_match = cat_name
                break

        price_match = re.search(r'(?:under|below|less than|max)\s*(?:₹|rs\.?|inr)?\s*([\d,]+)\s*(k|thousand)?', clean)
        max_price = None
        if price_match:
            base_num = float(price_match.group(1).replace(',', ''))
            is_k = price_match.group(2)
            max_price = base_num * 1000 if is_k or base_num < 100 else base_num

        if cat_match or (any(w in clean for w in ["find", "search", "show", "recommend", "looking for", "browse"]) and len(clean) < 60):
            query_term = re.sub(
                r'\b(find|search|show|recommend|me|some|under|below|less than|max|₹|rs\.?|inr|\d+|,|k|laptops?|smartphones?|mobiles?|phones?|headphones?|monitors?|keyboards?|mice|mouse|smartwatch(?:es)?)\b',
                '',
                clean,
            ).strip()
            products = await self.product_service.search_products(
                query=query_term if len(query_term) > 2 else None,
                category=cat_match,
                max_price=max_price,
                limit=3,
            )
            if not products and cat_match:
                products = await self.product_service.search_products(
                    category=cat_match,
                    max_price=max_price,
                    limit=3,
                )
            if products:
                price_note = f" under ₹{max_price:,.0f}" if max_price else ""
                cat_note = f" in {cat_match}" if cat_match else ""
                prod_bullets = "\n\n".join([
                    f"• **{p.name}** ({p.brand})\n  ₹{p.price:,.0f} | ⭐ {p.rating:.1f} | Stock: {p.inventory.quantity if p.inventory else 0} units | Warranty: {p.warranty}"
                    for p in products
                ])
                msg = f"Here are the top matches{cat_note}{price_note}:\n\n{prod_bullets}\n\nWould you like full specs on any of these, or to add one to your cart?"
                return {
                    "response": msg,
                    "products": [self._format_prod(p) for p in products],
                    "tool_activities": [
                        {"tool_name": "search_products", "status": "completed", "display_text": f"Found {len(products)} products"}
                    ],
                }

        # -------------------------------------------------------------
        # 9. Accurate Store Policy FAQs (Return, Shipping, Warranty, Payment)
        # -------------------------------------------------------------
        if any(p in clean for p in ["return", "refund", "exchange", "replacement"]):
            stmt = select(Document).where(or_(Document.category.in_(["returns", "refunds"]), Document.title.ilike("%Return%"))).limit(1)
            doc = (await self.session.execute(stmt)).scalars().first()
            if doc:
                return {
                    "response": f"**{doc.title}**\n\n{doc.content}\n\nWould you like help initiating a return for an order?",
                    "products": [],
                    "tool_activities": [
                        {"tool_name": "search_policies", "status": "completed", "display_text": "Retrieved Return Policy"}
                    ],
                }

        if any(p in clean for p in ["shipping", "delivery", "track shipping", "courier", "how long to deliver"]):
            stmt = select(Document).where(or_(Document.category.in_(["shipping", "delivery"]), Document.title.ilike("%Shipping%"))).limit(1)
            doc = (await self.session.execute(stmt)).scalars().first()
            if doc:
                return {
                    "response": f"**{doc.title}**\n\n{doc.content}\n\nLet me know if you need help with an existing order tracking number!",
                    "products": [],
                    "tool_activities": [
                        {"tool_name": "search_policies", "status": "completed", "display_text": "Retrieved Shipping Policy"}
                    ],
                }

        if any(p in clean for p in ["warranty", "guarantee", "repair"]):
            stmt = select(Document).where(or_(Document.category == "warranty", Document.title.ilike("%Warranty%"))).limit(1)
            doc = (await self.session.execute(stmt)).scalars().first()
            if doc:
                return {
                    "response": f"**{doc.title}**\n\n{doc.content}\n\nAll electronics sold on AgentCart come with genuine brand warranty.",
                    "products": [],
                    "tool_activities": [
                        {"tool_name": "search_policies", "status": "completed", "display_text": "Retrieved Warranty Policy"}
                    ],
                }

        if any(p in clean for p in ["payment", "cod", "emi", "upi", "credit card", "debit card"]):
            stmt = select(Document).where(or_(Document.category == "payment", Document.title.ilike("%Payment%"))).limit(1)
            doc = (await self.session.execute(stmt)).scalars().first()
            if doc:
                return {
                    "response": f"**{doc.title}**\n\n{doc.content}",
                    "products": [],
                    "tool_activities": [
                        {"tool_name": "search_policies", "status": "completed", "display_text": "Retrieved Payment Policy"}
                    ],
                }

        # Intent not matched by fast path -> Fallback to Ollama LLM
        return None

    def _format_prod(self, p) -> Dict[str, Any]:
        return {
            "id": p.id,
            "name": p.name,
            "brand": p.brand,
            "price": p.price,
            "rating": p.rating,
            "stock": p.inventory.quantity if p.inventory else 0,
            "warranty": p.warranty,
        }
