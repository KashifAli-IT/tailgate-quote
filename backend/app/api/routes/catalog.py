from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.services.calculation_service import calculate_line_item
from app.services.pricing_service import get_price_list


router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)


class CalculateLineItemRequest(BaseModel):
    sku: str = Field(min_length=1)
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)


@router.get("/search")
async def search_catalog(
    query: str = Query(..., min_length=1),
):
    return {
        "query": query,
        "items": get_price_list(query),
    }


@router.post("/calculate")
async def calculate_catalog_line_item(
    request: CalculateLineItemRequest,
):
    return calculate_line_item(
        sku=request.sku,
        quantity=request.quantity,
        unit_price=request.unit_price,
    )