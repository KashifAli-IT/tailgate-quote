from app.services.calculation_service import calculate_line_item
from app.storage.quote_store import (
    generate_quote_id,
    save_quote,
    get_saved_quote,
)


def create_draft_quote(
    customer_name: str,
    items: list[dict],
) -> dict:
    quote_id = generate_quote_id()

    calculated_items = []

    for item in items:
        calculated_item = calculate_line_item(
            sku=item["sku"],
            quantity=item["quantity"],
        )

        calculated_item["evidence"] = {
            "source_text": item.get("source_text"),
            "quantity_evidence": item.get("quantity_evidence"),
            "product_evidence": item.get("product_evidence"),
        }

        calculated_items.append(calculated_item)

    total = sum(
        item["subtotal"]
        for item in calculated_items
    )

    quote = {
        "quote_id": quote_id,
        "status": "DRAFT",
        "customer_name": customer_name,
        "items": calculated_items,
        "total": round(total, 2),
        "evidence_summary": {
            "source_evidence": True,
            "quantity_evidence": True,
            "product_evidence": True,
            "price_evidence": True,
            "calculation_evidence": True,
        },
    }

    save_quote(
        quote_id,
        quote,
    )

    return quote


def get_quote(quote_id: str) -> dict:
    quote = get_saved_quote(quote_id)

    if quote is None:
        raise ValueError(f"Quote not found: {quote_id}")

    return quote


def approve_quote(quote_id: str) -> dict:
    quote = get_saved_quote(quote_id)

    if quote is None:
        raise ValueError(f"Quote not found: {quote_id}")

    if quote["status"] != "DRAFT":
        raise ValueError(
            f"Quote cannot be approved from status: {quote['status']}"
        )

    quote["status"] = "APPROVED"

    save_quote(
        quote_id,
        quote,
    )

    return quote


def send_quote(quote_id: str) -> dict:
    quote = get_saved_quote(quote_id)

    if quote is None:
        raise ValueError(f"Quote not found: {quote_id}")

    if quote["status"] != "APPROVED":
        raise ValueError(
            f"Quote cannot be sent from status: {quote['status']}"
        )

    quote["status"] = "SENT"

    save_quote(
        quote_id,
        quote,
    )

    return quote