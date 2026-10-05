from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CatalogItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    category: str
    specification: str
    description: Optional[str] = None
    unit: str = "each"
    unit_price: float = 0.0


class CatalogItemCreate(BaseModel):
    sku: str
    category: str
    specification: str
    description: Optional[str] = None
    unit: str = "each"
    unit_price: float = 0.0