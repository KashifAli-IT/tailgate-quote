from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.quote_service import QuoteService
from ..services.evidence_service import EvidenceService
from ..schemas.tools import CreateDraftQuoteRequest


async def create_draft_quote(session: AsyncSession, arguments: Dict[str, Any]) -> Dict[str, Any]:
    request = CreateDraftQuoteRequest(**arguments)

    quote_service = QuoteService(session)
    quote = await quote_service.create_quote(
        customer_name=request.customer_name,
        customer_company=request.customer_company,
        job_address=request.job_address,
        job_description=request.job_description,
        line_items=request.line_items,
        labor_hours=request.labor_hours,
        labor_rate=request.labor_rate,
        notes=request.notes,
    )

    evidence_service = EvidenceService(session)
    for item in request.line_items:
        await evidence_service.add_evidence(
            quote_id=quote.id,
            field_name=f"line_item_{item['sku']}_quantity",
            field_value=str(item["quantity"]),
            source_type="transcript",
            source_text=f"quantity {item['quantity']}",
        )
        await evidence_service.add_evidence(
            quote_id=quote.id,
            field_name=f"line_item_{item['sku']}_unit_price",
            field_value=str(item["unit_price"]),
            source_type="catalog",
            source_text=f"SKU {item['sku']}",
        )

    quote = await quote_service.recalculate_totals(quote.id)

    # Re-fetch with items loaded
    quote = await quote_service.get_quote(quote.id)

    return {
        "success": True,
        "quote_id": quote.id,
        "quote_number": quote.quote_number,
        "status": quote.status,
        "line_items": [
            {
                "sku": item.catalog_sku,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal,
            }
            for item in quote.items
        ],
        "labor_hours": quote.labor_hours,
        "labor_rate": quote.labor_rate,
        "subtotal": quote.subtotal,
        "total": quote.total,
    }