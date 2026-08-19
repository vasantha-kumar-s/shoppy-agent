"""
AgentCart — High-Efficiency RAG Tools.
"""

from langchain_core.tools import tool
from app.database.connection import async_session_factory
from app.rag.retriever import PolicyRetriever


@tool
async def search_policies(query: str) -> dict:
    """Search store FAQ policies on returns, refunds, warranty, shipping, and delivery times."""
    async with async_session_factory() as session:
        retriever = PolicyRetriever(session)
        docs = await retriever.retrieve(query, top_k=2)
        return {"results": docs}
