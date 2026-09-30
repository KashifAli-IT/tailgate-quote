from decimal import Decimal, ROUND_HALF_UP

from app.services.pricing_service import load_catalog


def calculate_line_item(
    sku: str,
    quantity: int | float,
) -> dict:
    catalog_item = next(
        (
            item
            for item in load_catalog()
            if item["sku"].upper() == sku.upper()
        ),
        None,
    )

    if catalog_item is None:
        raise ValueError(f"Unknown SKU: {sku}")

    quantity_decimal = Decimal(str(quantity))
    unit_price_decimal = Decimal(
        str(catalog_item["unit_price"])
    )

    subtotal = (
        quantity_decimal * unit_price_decimal
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return {
        "sku": catalog_item["sku"],
        "quantity": quantity,
        "unit_price": float(unit_price_decimal),
        "subtotal": float(subtotal),
    }