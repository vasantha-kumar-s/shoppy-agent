"""
AgentCart — Agent State Definition.
"""

from typing import Annotated, Sequence, TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """The graph state holding message history and shopping context."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_id: int
    conversation_id: Optional[int]
    tool_activities: List[Dict[str, Any]]
    extracted_products: List[Dict[str, Any]]
