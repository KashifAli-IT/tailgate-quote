from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.pricing_service import PricingService
from ..services.calculation_service import LineItemCalculation
from ..schemas.tools import CalculateLineItemRequest


async def calculate_line_item(session: AsyncSession, arguments: Dict[str, Any]) -> Dict[str, Any]:
    request = CalculateLineItemRequest(**arguments)

    service = PricingService(session)
    catalog_item = await service.get_by_sku(request.sku)
    if catalog_item is None:
        return {
            "success": False,
            "error": f"SKU {request.sku} not found in catalog",
        }

    calc = LineItemCalculation.calculate(
        sku=request.sku,
        quantity=request.quantity,
        unit_price=request.unit_price,
    )

    return {
        "success": True,
        "sku": calc.sku,
        "quantity": calc.quantity,
        "unit_price": calc.unit_price,
        "subtotal": calc.subtotal,
        "catalog_description": catalog_item.description,
        "catalog_specification": catalog_item.specification,
        "catalog_unit": catalog_item.unit,
    }