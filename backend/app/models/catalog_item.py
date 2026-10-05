from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.database import Base


class CatalogItem(Base):
    __tablename__ = "catalog_items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    specification = Column(String, nullable=False)
    description = Column(String, nullable=True)
    unit = Column(String, nullable=False, default="each")
    unit_price = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    line_items = relationship("QuoteItem", back_populates="catalog_item")