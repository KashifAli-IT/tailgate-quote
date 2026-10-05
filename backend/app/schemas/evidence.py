from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class EvidenceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quote_id: int
    field_name: str
    field_value: str
    source_type: str  # transcript | catalog | calculation
    source_text: Optional[str] = None
    source_location: Optional[str] = None


class EvidenceListResponse(BaseModel):
    items: List[EvidenceSchema]