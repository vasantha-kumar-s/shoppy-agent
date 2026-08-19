"""
AgentCart — LangGraph Agent Definition.

Constructs the ReAct state machine connecting Ollama (ChatOllama),
tool node, conditional edges, and state memory.
"""

import logging
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.core.config import settings
from app.agents.state import AgentState
from app.agents.prompts import SYSTEM_PROMPT
from app.tools import ALL_TOOLS

logger = logging.getLogger(__name__)


def get_llm():
    """Instantiate ChatOllama bound with all agent tools optimized for speed."""
    llm = ChatOllama(
        base_url=settings.OLLAMA_HOST,
        model=settings.OLLAMA_MODEL,
        temperature=0.1,  # Low temperature for fast, deterministic tool calling
        num_ctx=2048,     # 2k context window fits completely in GPU VRAM for fast inference
        keep_alive="1h",  # Keep model warm in memory
        timeout=30.0,
    )
    return llm.bind_tools(ALL_TOOLS)


# Agent node: invokes LLM with full context
async def agent_node(state: AgentState) -> dict:
    """Agent node function that calls Ollama with bound tools."""
    llm = get_llm()
    messages = state["messages"]

    # Ensure system prompt is at the start
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    response = await llm.ainvoke(messages)
    return {"messages": [response]}


def create_agent_graph():
    """Build and compile the LangGraph ReAct agent graph."""
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(ALL_TOOLS))

    # Add Edges
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    return workflow.compile()


# Singleton compiled agent graph
agent_graph = create_agent_graph()
