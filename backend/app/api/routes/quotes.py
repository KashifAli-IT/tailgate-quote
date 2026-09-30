from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.quote_service import (
    approve_quote,
    create_draft_quote,
    get_quote,
)


router = APIRouter(
    prefix="/quotes",
    tags=["Quotes"],
)


class QuoteItemRequest(BaseModel):
    sku: str = Field(min_length=1)
    quantity: float = Field(gt=0)
    source_text: str | None = None
    quantity_evidence: str | None = None
    product_evidence: str | None = None


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
                    "source_text": item.source_text,
                    "quantity_evidence": item.quantity_evidence,
                    "product_evidence": item.product_evidence,
                }
                for item in request.items
            ],
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@router.get("/{quote_id}")
async def get_quote_by_id(
    quote_id: str,
):
    try:
        return get_quote(quote_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@router.post("/{quote_id}/approve")
async def approve_quote_by_id(
    quote_id: str,
):
    try:
        return approve_quote(quote_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )