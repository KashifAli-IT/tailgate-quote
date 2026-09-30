from app.services.calculation_service import calculate_line_item


_quotes: dict[str, dict] = {}
_next_quote_number = 1


def create_draft_quote(
    customer_name: str,
    items: list[dict],
) -> dict:
    global _next_quote_number

    quote_id = f"Q-{_next_quote_number:04d}"
    _next_quote_number += 1

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
    }

    _quotes[quote_id] = quote

    return quote

def get_quote(quote_id: str) -> dict:
    quote = _quotes.get(quote_id)

    if quote is None:
        raise ValueError(f"Quote not found: {quote_id}")

    return quote

def approve_quote(quote_id: str) -> dict:
    quote = _quotes.get(quote_id)

    if quote is None:
        raise ValueError(f"Quote not found: {quote_id}")

    if quote["status"] != "DRAFT":
        raise ValueError(
            f"Quote cannot be approved from status: {quote['status']}"
        )

    quote["status"] = "APPROVED"

    return quote