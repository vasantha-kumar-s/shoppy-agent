"""
AgentCart — Database Seeder.

Populates the database with:
- 2 demo users with addresses
- 7 categories
- 50+ products with inventory
- Product reviews
- Policy documents for RAG

Run: python -m seed.seed_data
"""

import asyncio
import logging
import random
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, text
from app.database.connection import async_session_factory, engine
from app.database.base import Base
from app.models import (
    User, Category, Product, Inventory, Cart,
    Address, Conversation, ProductReview, Document,
)
from seed.product_data import CATEGORIES, PRODUCTS
from seed.policy_data import POLICY_DOCUMENTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def seed_database():
    """Main seeder: creates tables and populates all data."""

    # Create tables
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Tables created")

    async with async_session_factory() as session:
        # Check if already seeded
        result = await session.execute(select(User).limit(1))
        if result.scalars().first():
            logger.info("⚠️  Database already seeded. Skipping.")
            return

        # --- 1. Users ---
        users = [
            User(name="Demo User", email="demo@agentcart.local"),
            User(name="Test Shopper", email="tester@agentcart.local"),
        ]
        session.add_all(users)
        await session.flush()
        logger.info(f"✅ Created {len(users)} users")

        # --- 2. Addresses ---
        addresses = [
            Address(
                user_id=users[0].id, label="Home",
                street="42, MG Road, Indiranagar",
                city="Bangalore", state="Karnataka", pincode="560038",
                is_default=True
            ),
            Address(
                user_id=users[0].id, label="Office",
                street="WeWork Galaxy, Residency Road",
                city="Bangalore", state="Karnataka", pincode="560025",
                is_default=False
            ),
            Address(
                user_id=users[1].id, label="Home",
                street="15, Connaught Place",
                city="New Delhi", state="Delhi", pincode="110001",
                is_default=True
            ),
        ]
        session.add_all(addresses)
        await session.flush()
        logger.info(f"✅ Created {len(addresses)} addresses")

        # --- 3. Carts (one per user) ---
        carts = [
            Cart(user_id=users[0].id),
            Cart(user_id=users[1].id),
        ]
        session.add_all(carts)
        await session.flush()
        logger.info(f"✅ Created {len(carts)} carts")

        # --- 4. Categories ---
        category_map = {}
        for cat_data in CATEGORIES:
            cat = Category(**cat_data)
            session.add(cat)
            await session.flush()
            category_map[cat.slug] = cat
        logger.info(f"✅ Created {len(category_map)} categories")

        # --- 5. Products + Inventory ---
        all_products = []
        for cat_slug, product_list in PRODUCTS.items():
            category = category_map[cat_slug]
            for prod_data in product_list:
                inv_qty = prod_data.pop("inventory", 50)
                product = Product(
                    name=prod_data["name"],
                    description=prod_data["description"],
                    brand=prod_data["brand"],
                    category_id=category.id,
                    price=prod_data["price"],
                    rating=prod_data["rating"],
                    specifications=prod_data.get("specifications"),
                    warranty=prod_data.get("warranty"),
                    image_url=None,  # Placeholder — no images in seed
                )
                session.add(product)
                await session.flush()

                # Create inventory
                inv = Inventory(product_id=product.id, quantity=inv_qty)
                session.add(inv)
                all_products.append(product)

        await session.flush()
        logger.info(f"✅ Created {len(all_products)} products with inventory")

        # --- 6. Product Reviews ---
        review_comments = [
            "Great product! Exactly as described.",
            "Good value for money. Recommended.",
            "Decent quality, works as expected.",
            "Excellent build quality and performance.",
            "Very happy with this purchase.",
            "A bit overpriced but works well.",
            "Perfect for daily use. No complaints.",
            "Superb! Exceeded my expectations.",
            "Good product, fast delivery.",
            "Solid performer, would buy again.",
        ]
        reviews = []
        for product in all_products:
            num_reviews = random.randint(1, 3)
            for _ in range(num_reviews):
                review = ProductReview(
                    product_id=product.id,
                    user_id=random.choice(users).id,
                    rating=round(random.uniform(3.0, 5.0), 1),
                    comment=random.choice(review_comments),
                )
                reviews.append(review)
        session.add_all(reviews)
        await session.flush()
        logger.info(f"✅ Created {len(reviews)} product reviews")

        # --- 7. Policy Documents (for RAG — embeddings added later) ---
        docs = []
        for doc_data in POLICY_DOCUMENTS:
            doc = Document(
                title=doc_data["title"],
                content=doc_data["content"],
                category=doc_data["category"],
                embedding=None,  # Embeddings populated in Phase 10
            )
            docs.append(doc)
        session.add_all(docs)
        await session.flush()
        logger.info(f"✅ Created {len(docs)} policy documents")

        # --- 8. Default conversation for demo user ---
        conv = Conversation(user_id=users[0].id, title="Welcome Chat")
        session.add(conv)
        await session.flush()
        logger.info("✅ Created default conversation")

        await session.commit()
        logger.info("🎉 Database seeding complete!")

        # Summary
        logger.info(f"\n📊 Seed Summary:")
        logger.info(f"   Users: {len(users)}")
        logger.info(f"   Addresses: {len(addresses)}")
        logger.info(f"   Categories: {len(category_map)}")
        logger.info(f"   Products: {len(all_products)}")
        logger.info(f"   Reviews: {len(reviews)}")
        logger.info(f"   Policy Documents: {len(docs)}")


if __name__ == "__main__":
    asyncio.run(seed_database())
