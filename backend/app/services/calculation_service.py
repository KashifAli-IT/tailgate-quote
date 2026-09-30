from decimal import Decimal, ROUND_HALF_UP


def calculate_line_item(
    sku: str,
    quantity: int | float,
    unit_price: str | float,
) -> dict:
    quantity_decimal = Decimal(str(quantity))
    unit_price_decimal = Decimal(str(unit_price))

    subtotal = (
        quantity_decimal * unit_price_decimal
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return {
        "sku": sku,
        "quantity": quantity,
        "unit_price": float(unit_price_decimal),
        "subtotal": float(subtotal),
    }