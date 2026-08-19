"""
AgentCart — Seed Data: Policy Documents for RAG.

Store policy content for the RAG retrieval system.
"""

POLICY_DOCUMENTS = [
    {
        "title": "Shipping Policy",
        "category": "shipping",
        "content": """AgentCart Shipping Policy

We offer multiple shipping options across India:

Standard Shipping:
- Delivery within 5-7 business days
- Free for orders above ₹999
- ₹49 flat fee for orders below ₹999

Express Shipping:
- Delivery within 2-3 business days
- ₹149 for orders below ₹1999
- ₹99 for orders above ₹1999

Same-Day Delivery:
- Available in select metros (Delhi, Mumbai, Bangalore, Chennai, Hyderabad, Kolkata)
- Orders placed before 12 PM qualify
- ₹299 delivery charge
- Free for orders above ₹9999

Shipping Tracking:
- All orders include tracking via SMS and email
- Track your order in the Orders section
- Estimated delivery date shown after order placement

Remote Areas:
- Delivery to remote pin codes may take 7-10 business days
- Additional charges may apply for remote locations"""
    },
    {
        "title": "Return Policy",
        "category": "returns",
        "content": """AgentCart Return Policy

Easy Returns within 7-30 days depending on product category:

Electronics (Laptops, Smartphones, Monitors):
- 7-day return window from delivery date
- Product must be unused and in original packaging
- All accessories and free gifts must be returned
- Opened software/sealed items cannot be returned

Accessories (Headphones, Keyboards, Mice, Smartwatches):
- 15-day return window from delivery date
- Product must be in original condition
- Original packaging required

How to Initiate a Return:
1. Go to Orders section
2. Select the order
3. Click "Return Item"
4. Choose a reason
5. Schedule pickup or drop at nearest center

Return Pickup:
- Free pickup available in most cities
- Pickup within 2-3 business days of return request
- Self-drop at partner stores also available

Exceptions (Non-returnable):
- Products with physical damage caused by customer
- Products without original packaging
- Customized or personalized products
- Products purchased during flash sales marked "non-returnable" """
    },
    {
        "title": "Refund Policy",
        "category": "refunds",
        "content": """AgentCart Refund Policy

Refund Timeline:
- Refund initiated within 24 hours of return pickup
- Bank account: 5-7 business days
- UPI: 2-3 business days
- Original payment method: 5-10 business days
- Store credit: Instant (upon return approval)

Refund Amount:
- Full refund for defective products
- Full refund for wrong product delivered
- Shipping charges refunded only if return is due to our error
- COD orders refunded to bank account or store credit

Partial Refund:
- Products returned with missing accessories: up to 15% deduction
- Products with signs of use: up to 20% deduction
- Damaged packaging (non-defective product): up to 10% deduction

Store Credit:
- Never expires
- Can be used on any product
- Cannot be converted to cash"""
    },
    {
        "title": "Warranty Policy",
        "category": "warranty",
        "content": """AgentCart Warranty Policy

All products sold on AgentCart carry manufacturer warranty:

Warranty Coverage by Category:
- Laptops: 1-2 years (varies by brand)
- Smartphones: 1 year manufacturer warranty
- Headphones: 1 year manufacturer warranty
- Monitors: 3 years (most brands)
- Keyboards: 1-2 years
- Mice: 1-2 years
- Smartwatches: 1 year

What's Covered:
- Manufacturing defects
- Hardware malfunctions under normal use
- Dead pixels (above threshold defined by manufacturer)
- Battery defects within warranty period

What's NOT Covered:
- Physical damage (drops, water damage, cracks)
- Damage from unauthorized repair
- Normal wear and tear
- Software issues
- Accessories (chargers, cables) after 6 months

How to Claim Warranty:
1. Contact the brand's service center directly
2. Or raise a warranty claim through AgentCart support
3. Provide proof of purchase (order confirmation email or invoice)
4. Brand service center will inspect and repair/replace

Extended Warranty:
- Available for select products at checkout
- Extends coverage by 1 additional year
- Covers accidental damage (screen cracks, liquid spills)"""
    },
    {
        "title": "Delivery Times",
        "category": "delivery",
        "content": """AgentCart Delivery Time Guide

Estimated delivery times by region:

Metro Cities (Delhi, Mumbai, Bangalore, Chennai, Hyderabad, Kolkata, Pune):
- Standard: 3-5 business days
- Express: 1-2 business days
- Same-day: Available (order before 12 PM)

Tier 2 Cities (Jaipur, Lucknow, Ahmedabad, Chandigarh, Kochi, etc.):
- Standard: 5-7 business days
- Express: 2-3 business days

Tier 3 Cities and Towns:
- Standard: 7-10 business days
- Express: 3-5 business days

Remote/Rural Areas:
- Standard: 10-15 business days
- Express: Not available in all locations

Factors Affecting Delivery:
- Product availability (in-stock vs. made-to-order)
- Weather conditions and natural disasters
- Public holidays and weekends
- Address verification issues
- Customs processing (for imported items)

Pre-order Items:
- Delivery date mentioned on product page
- Email notification sent when item ships"""
    },
    {
        "title": "Cancellation Policy",
        "category": "cancellation",
        "content": """AgentCart Order Cancellation Policy

You can cancel your order based on its current status:

Before Shipping:
- Cancel for free anytime before the order is shipped
- Full refund to original payment method
- Cancel from the Orders section or contact support

After Shipping (In Transit):
- Cancellation may not be possible once shipped
- You can refuse delivery and it will be treated as a return
- Return shipping may be charged

After Delivery:
- Use our Return Policy instead
- 7-30 day return window based on product category

Automatic Cancellation:
- Orders with payment pending for more than 24 hours are auto-cancelled
- Out-of-stock items will be cancelled with full refund

Partial Cancellation:
- You can cancel individual items from a multi-item order
- Remaining items will still be delivered
- Shipping charges recalculated based on remaining order value

Refund on Cancellation:
- Prepaid orders: Refund within 5-7 business days
- COD orders: No charge (not yet paid)
- EMI orders: EMI cancelled and refunded per bank policies"""
    },
    {
        "title": "Payment FAQ",
        "category": "payment",
        "content": """AgentCart Payment Information

Note: AgentCart is a demo application. All payments and orders are simulated.
No real money is charged. No real payment gateway is connected.

Simulated Payment Methods (for demo purposes):
- Credit/Debit Card (simulated)
- UPI (simulated)
- Net Banking (simulated)
- Cash on Delivery (simulated)
- EMI (simulated)

In the demo:
- Orders are created with "confirmed" status immediately
- No actual payment processing occurs
- Cart is cleared after order placement
- Order tracking shows simulated status updates

Security (in production):
- All payment pages would use SSL/TLS encryption
- Card details would never be stored on our servers
- PCI-DSS compliance required for real payment processing
- OTP verification for all transactions"""
    },
    {
        "title": "General FAQ",
        "category": "faq",
        "content": """AgentCart — Frequently Asked Questions

Q: Is AgentCart a real e-commerce store?
A: No, AgentCart is a demo/portfolio project showcasing AI-powered shopping assistance. No real products are sold or shipped.

Q: How does the AI assistant work?
A: The AI assistant uses a local LLM (via Ollama) with tool calling capabilities. It can search products, manage your cart, create orders, and answer policy questions — all through natural conversation.

Q: What is "tool calling"?
A: Tool calling means the AI can decide to call specific functions (like searching products or checking stock) rather than just generating text. This ensures accurate, up-to-date information from the database.

Q: Can I use voice to interact?
A: Yes! Click the microphone button to speak. Your speech is transcribed locally using faster-whisper. The AI can also respond with synthesized speech using Kokoro TTS.

Q: Do I need an internet connection?
A: The core application runs entirely locally — LLM, speech services, and database are all self-hosted. No external API calls to OpenAI or other cloud services.

Q: What LLM models are supported?
A: Any Ollama-compatible model with tool calling support. Default is qwen2.5:7b. You can change the model via the OLLAMA_MODEL environment variable.

Q: How is my data stored?
A: All data is stored in a local PostgreSQL database. Conversations, cart, and orders persist between sessions.

Q: Can I return a product?
A: In the demo, orders are simulated and returns are not processed. See our Return Policy for what a real implementation would look like.

Q: How accurate are product recommendations?
A: The AI searches real product data in the database using your criteria. It never invents products or prices — all information comes from tool calls to the database.

Q: Is my voice data sent to any cloud service?
A: No. All voice processing happens locally via faster-whisper (STT) and Kokoro (TTS) running as Docker containers on your machine."""
    },
]
