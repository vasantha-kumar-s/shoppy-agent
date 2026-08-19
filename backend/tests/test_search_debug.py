import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from app.database.connection import async_session_factory
from app.services.product_service import ProductService

async def main():
    async with async_session_factory() as session:
        service = ProductService(session)
        p1 = await service.search_products(query='wireless', category='headphones', max_price=5000.0)
        print("Search with query='wireless', category='headphones', max_price=5000.0:")
        for p in p1:
            print(f"  - {p.name} (₹{p.price})")

        p2 = await service.search_products(category='headphones', max_price=5000.0)
        print("\nSearch with category='headphones', max_price=5000.0:")
        for p in p2:
            print(f"  - {p.name} (₹{p.price})")

if __name__ == "__main__":
    asyncio.run(main())
