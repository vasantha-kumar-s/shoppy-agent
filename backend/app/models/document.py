"""Document model for RAG — stores policy documents with embeddings or text fallback."""

import os
import datetime
from sqlalchemy import String, Text, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

# Allow disabling pgvector for local PostgreSQL instances without pgvector compiled
USE_PGVECTOR = os.getenv("USE_PGVECTOR", "false").lower() in ("true", "1")

if USE_PGVECTOR:
    try:
        from pgvector.sqlalchemy import Vector
        EmbeddingType = Vector(768)
    except Exception:
        EmbeddingType = JSON
else:
    EmbeddingType = JSON


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    embedding = mapped_column(EmbeddingType, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<Document id={self.id} title={self.title!r}>"
