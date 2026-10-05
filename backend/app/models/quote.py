from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    quote_number = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="DRAFT", index=True)
    customer_name = Column(String, nullable=True)
    customer_company = Column(String, nullable=True)
    job_address = Column(String, nullable=True)
    job_description = Column(String, nullable=True)
    labor_rate = Column(Float, default=0.0)
    labor_hours = Column(Float, default=0.0)
    subtotal = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    sent_at = Column(DateTime(timezone=True), nullable=True)

    items = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="quote", cascade="all, delete-orphan")