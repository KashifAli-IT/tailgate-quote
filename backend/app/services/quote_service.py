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
        calculated_items.append(
            calculate_line_item(
                sku=item["sku"],
                quantity=item["quantity"],
            )
        )

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