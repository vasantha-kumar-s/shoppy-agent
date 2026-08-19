"""
AgentCart — Conversation Memory Service.

Persists conversations and messages in PostgreSQL.
Loads recent chat context for LangGraph state initialization.
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation, Message
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

logger = logging.getLogger(__name__)


class MemoryService:
    """Service to manage conversation persistence and history loading."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_conversation(
        self, user_id: int, conversation_id: Optional[int] = None, title: str = "New Shopping Chat"
    ) -> Conversation:
        """Fetch existing conversation or create a new one."""
        if conversation_id:
            conv = await self.db.get(Conversation, conversation_id)
            if conv and conv.user_id == user_id:
                return conv

        # Create new conversation
        conv = Conversation(user_id=user_id, title=title)
        self.db.add(conv)
        await self.db.flush()
        return conv

    async def save_message(
        self, conversation_id: int, role: str, content: str, metadata: Optional[dict] = None
    ) -> Message:
        """Save a message to the database."""
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata_=metadata or {},
        )
        self.db.add(msg)
        await self.db.flush()
        return msg

    async def get_conversation_messages(
        self, conversation_id: int, limit: int = 20
    ) -> List[BaseMessage]:
        """Load recent messages converted to LangChain message objects."""
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        res = await self.db.execute(stmt)
        db_messages = list(res.scalars().all())
        db_messages.reverse()  # Chronological order

        lc_messages = []
        for m in db_messages:
            if m.role == "user":
                lc_messages.append(HumanMessage(content=m.content))
            elif m.role == "assistant":
                lc_messages.append(AIMessage(content=m.content))

        return lc_messages

    async def get_raw_messages(self, conversation_id: int, user_id: int) -> List[Dict[str, Any]]:
        """Load all raw messages for a conversation formatted for UI rendering."""
        conv = await self.db.get(Conversation, conversation_id)
        if not conv or conv.user_id != user_id:
            return []

        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        res = await self.db.execute(stmt)
        messages = res.scalars().all()

        return [
            {
                "id": str(m.id),
                "role": m.role,
                "content": m.content,
                "metadata": m.metadata_ or {},
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ]

    async def list_user_conversations(self, user_id: int) -> List[Dict[str, Any]]:
        """List all conversations for a user with message counts."""
        stmt = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        res = await self.db.execute(stmt)
        convs = res.scalars().all()

        out = []
        for c in convs:
            msg_stmt = select(Message).where(Message.conversation_id == c.id)
            msg_res = await self.db.execute(msg_stmt)
            count = len(msg_res.scalars().all())
            out.append({
                "id": c.id,
                "title": c.title or "Shopping Session",
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "message_count": count,
            })
        return out

    async def delete_conversation(self, conversation_id: int, user_id: int) -> bool:
        """Delete a conversation and its messages."""
        conv = await self.db.get(Conversation, conversation_id)
        if not conv or conv.user_id != user_id:
            return False

        # Delete messages first
        await self.db.execute(delete(Message).where(Message.conversation_id == conversation_id))
        # Delete conversation
        await self.db.delete(conv)
        await self.db.commit()
        return True
