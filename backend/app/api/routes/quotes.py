from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.quote_service import create_draft_quote


router = APIRouter(
    prefix="/quotes",
    tags=["Quotes"],
)


class QuoteItemRequest(BaseModel):
    sku: str = Field(min_length=1)
    quantity: float = Field(gt=0)


class CreateDraftQuoteRequest(BaseModel):
    customer_name: str = Field(min_length=1)
    items: list[QuoteItemRequest] = Field(min_length=1)


@router.post("/draft")
async def create_quote(
    request: CreateDraftQuoteRequest,
):
    try:
        return create_draft_quote(
            customer_name=request.customer_name,
            items=[
                {
                    "sku": item.sku,
                    "quantity": item.quantity,
                }
                for item in request.items
            ],
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )