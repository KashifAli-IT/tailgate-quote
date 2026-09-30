from fastapi import APIRouter, Query

from app.services.pricing_service import get_price_list


router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)


@router.get("/search")
async def search_catalog(
    query: str = Query(..., min_length=1),
):
    return {
        "query": query,
        "items": get_price_list(query),
    }