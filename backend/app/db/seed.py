from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.catalog_item import CatalogItem


SEED_CATALOG: List[dict] = [
    {
        "sku": "CP-075",
        "category": "copper_pipe",
        "specification": "3/4 inch",
        "description": "3/4 inch Type L Copper Pipe",
        "unit": "ft",
        "unit_price": 8.50,
    },
    {
        "sku": "CP-100",
        "category": "copper_pipe",
        "specification": "1 inch",
        "description": "1 inch Type L Copper Pipe",
        "unit": "ft",
        "unit_price": 12.00,
    },
    {
        "sku": "CP-050",
        "category": "copper_pipe",
        "specification": "1/2 inch",
        "description": "1/2 inch Type L Copper Pipe",
        "unit": "ft",
        "unit_price": 6.50,
    },
    {
        "sku": "PP-075",
        "category": "pex_pipe",
        "specification": "3/4 inch",
        "description": "3/4 inch PEX Pipe",
        "unit": "ft",
        "unit_price": 4.00,
    },
    {
        "sku": "SV-075",
        "category": "shutoff_valve",
        "specification": "3/4 inch",
        "description": "3/4 inch Shutoff Valve",
        "unit": "each",
        "unit_price": 24.00,
    },
    {
        "sku": "SV-100",
        "category": "shutoff_valve",
        "specification": "1 inch",
        "description": "1 inch Shutoff Valve",
        "unit": "each",
        "unit_price": 28.00,
    },
    {
        "sku": "LAB-STD",
        "category": "labor",
        "specification": "standard",
        "description": "Standard Labor",
        "unit": "hour",
        "unit_price": 120.00,
    },
    {
        "sku": "ELB-075",
        "category": "elbow",
        "specification": "3/4 inch",
        "description": "3/4 inch 90 Degree Copper Elbow",
        "unit": "each",
        "unit_price": 8.00,
    },
    {
        "sku": "CAP-075",
        "category": "cap",
        "specification": "3/4 inch",
        "description": "3/4 inch Copper Cap",
        "unit": "each",
        "unit_price": 6.00,
    },
    {
        "sku": "UNI-001",
        "category": "union",
        "specification": "3/4 inch",
        "description": "3/4 inch Copper Union",
        "unit": "each",
        "unit_price": 12.00,
    },
]


async def seed_catalog(session: AsyncSession) -> None:
    from sqlalchemy import select

    result = await session.execute(select(CatalogItem))
    existing = result.scalars().first()
    if existing is not None:
        return

    for item in SEED_CATALOG:
        catalog_item = CatalogItem(**item)
        session.add(catalog_item)

    await session.commit()