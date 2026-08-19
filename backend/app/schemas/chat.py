"""
AgentCart — Pydantic Schemas for Chat / Agent.
"""

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """User message to the agent."""
    message: str
    user_id: int = 1
    conversation_id: Optional[int] = None


class ToolActivity(BaseModel):
    """Represents a tool the agent used during processing."""
    tool_name: str
    status: str  # "running", "completed", "error"
    display_text: str  # User-facing text like "Searching products..."


class ChatResponse(BaseModel):
    """Agent response to user."""
    response: str
    conversation_id: int
    tool_activities: list[ToolActivity] = []
    products: list[dict] = []  # Product data shown inline
    metadata: dict = {}


class ConversationOut(BaseModel):
    """Conversation summary."""
    id: int
    title: str
    created_at: Optional[str] = None
    message_count: int = 0

    model_config = {"from_attributes": True}


class MessageOut(BaseModel):
    """Single message in a conversation."""
    id: int
    role: str
    content: str
    metadata_: Optional[dict] = None
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}
