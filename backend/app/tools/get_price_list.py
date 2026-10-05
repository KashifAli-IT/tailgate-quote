from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.pricing_service import PricingService
from ..schemas.tools import GetPriceListRequest


async def get_price_list(session: AsyncSession, arguments: Dict[str, Any]) -> Dict[str, Any]:
    request = GetPriceListRequest(**arguments)
    service = PricingService(session)

    found: List[dict] = []
    for item in request.items:
        category = item.get("category")
        specification = item.get("specification")
        results = await service.search(
            category=category,
            specification=specification,
        )
        for r in results:
            found.append(
                {
                    "sku": r.sku,
                    "category": r.category,
                    "specification": r.specification,
                    "description": r.description,
                    "unit": r.unit,
                    "unit_price": r.unit_price,
                }
            )

    return {
        "success": True,
        "items": found,
        "count": len(found),
    }