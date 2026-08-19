"""Product model."""

import datetime
from sqlalchemy import String, Text, Float, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    specifications: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    warranty: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    category = relationship("Category", back_populates="products", lazy="selectin")
    inventory = relationship("Inventory", back_populates="product", uselist=False, lazy="selectin")
    reviews = relationship("ProductReview", back_populates="product", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r} price={self.price}>"
