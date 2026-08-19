"""
AgentCart — Hybrid Fast-Path & LangGraph Streaming Chat API.
"""

import json
import re
import logging
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from app.database.connection import get_db, async_session_factory
from app.api.deps import get_current_user_id
from app.schemas.chat import ChatRequest, ChatResponse, ToolActivity, ConversationOut
from app.services.memory_service import MemoryService
from app.services.product_service import ProductService
from app.services.fast_intent_service import FastIntentService
from app.agents.graph import agent_graph

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Chat"])


def get_display_text_for_tool(tool_name: str, args: dict = None) -> str:
    """Generate clean, user-friendly activity text for each tool."""
    mapping = {
        "search_products": "Searching product catalog...",
        "get_product_details": "Fetching product specifications...",
        "compare_products": "Comparing products side by side...",
        "check_stock": "Checking real-time stock...",
        "get_cart": "Viewing shopping cart...",
        "add_to_cart": "Adding item to your cart...",
        "remove_from_cart": "Removing item from cart...",
        "update_cart_quantity": "Updating item quantity...",
        "clear_cart": "Clearing shopping cart...",
        "create_order": "Creating simulated order...",
        "get_order_status": "Checking order tracking...",
        "get_order_history": "Fetching order history...",
        "search_policies": "Retrieving store policy & FAQs...",
    }
    base = mapping.get(tool_name, f"Executing {tool_name}...")
    if args and isinstance(args, dict):
        if "query" in args and args["query"]:
            return f"Searching for \"{args['query']}\"..."
        if "product_id" in args:
            return f"Checking product #{args['product_id']}..."
    return base


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    req: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Chat with the AgentCart assistant using Fast-Path + LangGraph hybrid architecture."""
    memory = MemoryService(db)

    # 1. Get or create persistent conversation
    conv = await memory.get_or_create_conversation(
        user_id=user_id,
        conversation_id=req.conversation_id,
        title=req.message[:30] + ("..." if len(req.message) > 30 else ""),
    )

    # 2. Try instant Fast-Path intent matching (<100ms)
    fast_service = FastIntentService(db)
    fast_result = await fast_service.try_resolve_intent(
        req.message, user_id=user_id, conversation_id=conv.id
    )

    if fast_result:
        # Save messages to history
        await memory.save_message(conv.id, role="user", content=req.message)
        await memory.save_message(
            conv.id,
            role="assistant",
            content=fast_result["response"],
            metadata={"tools": [t["tool_name"] for t in fast_result.get("tool_activities", [])]},
        )
        await db.commit()

        return ChatResponse(
            response=fast_result["response"],
            conversation_id=conv.id,
            tool_activities=[ToolActivity(**t) for t in fast_result.get("tool_activities", [])],
            products=fast_result.get("products", []),
            metadata={"fast_path": True},
        )

    # 3. Fallback to LangGraph Agent for open-ended conversation
    history = await memory.get_conversation_messages(conv.id, limit=6)
    current_human_msg = HumanMessage(content=req.message)
    all_messages = history + [current_human_msg]

    tool_activities = []
    extracted_products = []
    final_response_text = ""

    try:
        result = await agent_graph.ainvoke({
            "messages": all_messages,
            "user_id": user_id,
            "conversation_id": conv.id,
            "tool_activities": [],
            "extracted_products": [],
        })

        for msg in result.get("messages", []):
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    name = tc.get("name", "")
                    args = tc.get("args", {})
                    tool_activities.append(
                        ToolActivity(
                            tool_name=name,
                            status="completed",
                            display_text=get_display_text_for_tool(name, args),
                        )
                    )

            if isinstance(msg, ToolMessage):
                content = msg.content
                if isinstance(content, dict) and "products" in content:
                    extracted_products.extend(content["products"])

            if isinstance(msg, AIMessage) and msg.content and not (hasattr(msg, "tool_calls") and msg.tool_calls):
                final_response_text = msg.content

        if not final_response_text:
            for msg in reversed(result.get("messages", [])):
                if isinstance(msg, AIMessage) and msg.content:
                    final_response_text = msg.content
                    break

    except Exception as e:
        logger.error(f"LangGraph Agent invocation error: {e}", exc_info=True)
        final_response_text = (
            "I could not connect to the local Ollama LLM service. "
            "Please ensure Ollama is running (`ollama run qwen2.5-coder:7b`)."
        )

    # Save messages
    await memory.save_message(conv.id, role="user", content=req.message)
    await memory.save_message(
        conv.id,
        role="assistant",
        content=final_response_text,
        metadata={"tools": [t.tool_name for t in tool_activities]},
    )
    await db.commit()

    return ChatResponse(
        response=final_response_text,
        conversation_id=conv.id,
        tool_activities=tool_activities,
        products=extracted_products[:6],
        metadata={"fast_path": False},
    )


@router.post("/chat/stream")
async def chat_stream_endpoint(
    req: ChatRequest,
    user_id: int = Depends(get_current_user_id),
):
    """Server-Sent Events (SSE) streaming endpoint with Fast-Path acceleration."""
    async def event_generator() -> AsyncGenerator[str, None]:
        async with async_session_factory() as session:
            memory = MemoryService(session)
            conv = await memory.get_or_create_conversation(
                user_id=user_id,
                conversation_id=req.conversation_id,
                title=req.message[:30] + ("..." if len(req.message) > 30 else ""),
            )

            # Yield conversation ID
            yield f"data: {json.dumps({'type': 'init', 'conversation_id': conv.id})}\n\n"

            # 1. Try Fast-Path intent (<100ms)
            fast_service = FastIntentService(session)
            fast_result = await fast_service.try_resolve_intent(
                req.message, user_id=user_id, conversation_id=conv.id
            )

            if fast_result:
                for act in fast_result.get("tool_activities", []):
                    yield f"data: {json.dumps({'type': 'tool_activity', 'tool_name': act['tool_name'], 'display_text': act['display_text']})}\n\n"

                await memory.save_message(conv.id, role="user", content=req.message)
                await memory.save_message(
                    conv.id,
                    role="assistant",
                    content=fast_result["response"],
                    metadata={"tools": [t["tool_name"] for t in fast_result.get("tool_activities", [])]},
                )
                await session.commit()

                yield f"data: {json.dumps({'type': 'done', 'response': fast_result['response'], 'products': fast_result.get('products', []), 'tool_activities': fast_result.get('tool_activities', []), 'conversation_id': conv.id})}\n\n"
                return

            # 2. Fallback to LangGraph streaming
            yield f"data: {json.dumps({'type': 'status', 'text': 'Analyzing shopping request with LLM...'})}\n\n"

            history = await memory.get_conversation_messages(conv.id, limit=6)
            current_human_msg = HumanMessage(content=req.message)
            all_messages = history + [current_human_msg]

            tool_activities = []
            extracted_products = []
            final_response_text = ""

            try:
                async for chunk in agent_graph.astream({
                    "messages": all_messages,
                    "user_id": user_id,
                    "conversation_id": conv.id,
                    "tool_activities": [],
                    "extracted_products": [],
                }, stream_mode="updates"):
                    for node_name, state_update in chunk.items():
                        if node_name == "agent":
                            messages = state_update.get("messages", [])
                            for msg in messages:
                                if hasattr(msg, "tool_calls") and msg.tool_calls:
                                    for tc in msg.tool_calls:
                                        t_name = tc.get("name", "")
                                        t_args = tc.get("args", {})
                                        display = get_display_text_for_tool(t_name, t_args)
                                        tool_activities.append(ToolActivity(
                                            tool_name=t_name,
                                            status="running",
                                            display_text=display,
                                        ))
                                        yield f"data: {json.dumps({'type': 'tool_activity', 'tool_name': t_name, 'display_text': display})}\n\n"
                                elif isinstance(msg, AIMessage) and msg.content:
                                    final_response_text = msg.content

                        elif node_name == "tools":
                            messages = state_update.get("messages", [])
                            for msg in messages:
                                if isinstance(msg, ToolMessage):
                                    content = msg.content
                                    if isinstance(content, dict) and "products" in content:
                                        new_prods = content["products"]
                                        extracted_products.extend(new_prods)
                                        yield f"data: {json.dumps({'type': 'products_found', 'count': len(new_prods)})}\n\n"

            except Exception as e:
                logger.error(f"Stream error: {e}", exc_info=True)
                final_response_text = "I encountered an issue processing your request. Please try again."

            await memory.save_message(conv.id, role="user", content=req.message)
            await memory.save_message(
                conv.id,
                role="assistant",
                content=final_response_text,
                metadata={"tools": [t.tool_name for t in tool_activities]},
            )
            await session.commit()

            yield f"data: {json.dumps({'type': 'done', 'response': final_response_text, 'products': extracted_products[:6], 'tool_activities': [t.model_dump() for t in tool_activities], 'conversation_id': conv.id})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/conversations", response_model=list[ConversationOut])
async def list_conversations(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List all saved conversations for the current user."""
    memory = MemoryService(db)
    convs = await memory.list_user_conversations(user_id)
    return [
        ConversationOut(
            id=c["id"],
            title=c["title"],
            created_at=c["created_at"],
            message_count=c["message_count"],
        )
        for c in convs
    ]


@router.post("/conversations", response_model=ConversationOut)
async def create_conversation_endpoint(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new empty chat session."""
    memory = MemoryService(db)
    conv = await memory.get_or_create_conversation(user_id=user_id, conversation_id=None, title="New Shopping Session")
    await db.commit()
    return ConversationOut(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at.isoformat() if conv.created_at else None,
        message_count=0,
    )


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages_endpoint(
    conversation_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Fetch all messages for a specific conversation session."""
    memory = MemoryService(db)
    messages = await memory.get_raw_messages(conversation_id, user_id)
    return {"conversation_id": conversation_id, "messages": messages}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation_endpoint(
    conversation_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation session."""
    memory = MemoryService(db)
    success = await memory.delete_conversation(conversation_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"deleted": True, "conversation_id": conversation_id}

