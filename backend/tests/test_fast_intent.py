import asyncio
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from app.database.connection import async_session_factory
from app.services.fast_intent_service import FastIntentService
from app.services.memory_service import MemoryService

async def main():
    test_queries = [
        "Show me all the items in the products.",
        "Show me mobiles.",
        "Add Samsung Galaxy S24 to the card.",
        "Show me the card",
        "place the order",
    ]

    async with async_session_factory() as session:
        memory = MemoryService(session)
        conv = await memory.get_or_create_conversation(user_id=1, conversation_id=None, title="User Transcript Flow")
        service = FastIntentService(session)

        for q in test_queries:
            t0 = time.time()
            res = await service.try_resolve_intent(q, user_id=1, conversation_id=conv.id)
            dt = time.time() - t0
            print("=" * 60)
            print(f"👤 User: \"{q}\"")
            print(f"⚡ Latency: {dt*1000:.1f}ms ({dt:.3f}s)")
            if res:
                print(f"🛒 Response:\n{res['response']}")
                await memory.save_message(conv.id, "user", q)
                await memory.save_message(conv.id, "assistant", res["response"])
                await session.commit()
            else:
                print("❌ Fallback to LLM")

if __name__ == "__main__":
    asyncio.run(main())
