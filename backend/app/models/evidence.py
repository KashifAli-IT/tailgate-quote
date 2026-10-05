from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    field_name = Column(String, nullable=False)
    field_value = Column(String, nullable=False)
    source_type = Column(String, nullable=False)  # transcript | catalog | calculation
    source_text = Column(String, nullable=True)
    source_location = Column(String, nullable=True)  # e.g. "turn 3"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    quote = relationship("Quote", back_populates="evidence")