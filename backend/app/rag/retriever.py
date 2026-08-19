"""
AgentCart — RAG Retriever.

Retrieves policy documents using pgvector similarity search or text fallback.
"""

import logging
from typing import List, Dict, Any
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.rag.embeddings import get_embedding

logger = logging.getLogger(__name__)


class PolicyRetriever:
    """RAG Retriever for store policies and FAQ."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Retrieve most relevant policy documents for the given query."""
        results = []

        # 1. Try vector similarity search with pgvector if embedding model is available
        query_vector = await get_embedding(query)
        if query_vector:
            try:
                # pgvector cosine distance: <=> operator
                stmt = (
                    select(Document)
                    .where(Document.embedding != None)
                    .order_by(Document.embedding.cosine_distance(query_vector))
                    .limit(top_k)
                )
                res = await self.db.execute(stmt)
                docs = res.scalars().all()
                if docs:
                    return [
                        {
                            "id": d.id,
                            "title": d.title,
                            "category": d.category,
                            "content": d.content,
                        }
                        for d in docs
                    ]
            except Exception as e:
                logger.warning(f"Vector search failed ({e}), falling back to keyword search.")

        # 2. Text keyword fallback
        words = [w.lower() for w in query.split() if len(w) > 2]
        if words:
            conditions = []
            for w in words:
                conditions.append(func.lower(Document.title).like(f"%{w}%"))
                conditions.append(func.lower(Document.content).like(f"%{w}%"))
                conditions.append(func.lower(Document.category).like(f"%{w}%"))

            stmt = select(Document).where(or_(*conditions)).limit(top_k)
            res = await self.db.execute(stmt)
            docs = res.scalars().all()
            if docs:
                return [
                    {
                        "id": d.id,
                        "title": d.title,
                        "category": d.category,
                        "content": d.content,
                    }
                    for d in docs
                ]

        # 3. Default: Return general FAQ and policies
        stmt = select(Document).limit(top_k)
        res = await self.db.execute(stmt)
        docs = res.scalars().all()
        return [
            {
                "id": d.id,
                "title": d.title,
                "category": d.category,
                "content": d.content,
            }
            for d in docs
        ]
