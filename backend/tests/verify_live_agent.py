"""
AgentCart — Live Agent & Ollama Verification Script.

Tests actual live inference with the configured Ollama model (qwen3:8b),
tool execution, and response synthesis.
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from langchain_core.messages import HumanMessage
from app.agents.graph import agent_graph
from app.core.config import settings


async def test_live_agent():
    print("=" * 60)
    print(f"Testing Live Agent with Ollama Model: {settings.OLLAMA_MODEL}")
    print(f"Ollama Host: {settings.OLLAMA_HOST}")
    print("=" * 60)

    test_queries = [
        "Find laptops under ₹70,000 for Python programming.",
        "What is the return policy for electronics?",
        "Hello! What can you help me with?",
    ]

    for idx, query in enumerate(test_queries, 1):
        print(f"\n[Test {idx}] User Query: \"{query}\"")
        print("-" * 50)

        state = {
            "messages": [HumanMessage(content=query)],
            "user_id": 1,
            "conversation_id": 1,
            "tool_activities": [],
            "extracted_products": [],
        }

        try:
            result = await agent_graph.ainvoke(state)
            messages = result.get("messages", [])

            # Print tool calls if any
            for msg in messages:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"  ⚙️ Tool Called: {tc.get('name')} with args {tc.get('args')}")

            # Print final assistant response
            final_msg = messages[-1]
            print(f"\n  🤖 Agent Response:\n{final_msg.content}\n")
            print("  ✅ PASS")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")

    print("\n" + "=" * 60)
    print("Live Agent Verification Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_live_agent())
