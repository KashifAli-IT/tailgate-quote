from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class QuoteItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quote_id: int
    catalog_sku: str
    quantity: float
    unit_price: float
    subtotal: float
    description_override: Optional[str] = None


class QuoteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quote_number: str
    status: str
    customer_name: Optional[str] = None
    customer_company: Optional[str] = None
    job_address: Optional[str] = None
    job_description: Optional[str] = None
    labor_rate: float = 0.0
    labor_hours: float = 0.0
    subtotal: float = 0.0
    total: float = 0.0
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    items: List[QuoteItemSchema] = []