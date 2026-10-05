import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.db.database import Base
from app.services.pricing_service import PricingService
from app.services.calculation_service import LineItemCalculation, QuoteTotals
from app.db.seed import SEED_CATALOG
from app.models.catalog_item import CatalogItem
from app.tools import execute_tool


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
TestSessionMaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class TestBase:
    @pytest.fixture(autouse=True)
    async def setup_database(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @pytest.fixture
    async def session(self):
        async with TestSessionMaker() as session:
            yield session

    @pytest.fixture
    async def seeded_session(self, session):
        for item in SEED_CATALOG:
            session.add(CatalogItem(**item))
        await session.commit()
        return session


class TestPricing(TestBase):
    async def test_list_all(self, seeded_session):
        service = PricingService(seeded_session)
        items = await service.list_all()
        assert len(items) == len(SEED_CATALOG)

    async def test_get_by_sku(self, seeded_session):
        service = PricingService(seeded_session)
        item = await service.get_by_sku("CP-075")
        assert item is not None
        assert item.sku == "CP-075"
        assert item.unit_price == 8.50

    async def test_get_by_sku_not_found(self, seeded_session):
        service = PricingService(seeded_session)
        item = await service.get_by_sku("NONEXISTENT")
        assert item is None

    async def test_search_by_category(self, seeded_session):
        service = PricingService(seeded_session)
        items = await service.search(category="copper_pipe")
        assert len(items) == 3

    async def test_search_by_specification(self, seeded_session):
        service = PricingService(seeded_session)
        items = await service.search(specification="3/4 inch")
        assert len(items) == 6


class TestCalculations(TestBase):
    def test_line_item_calculation(self):
        calc = LineItemCalculation.calculate("CP-075", 18, 8.50)
        assert calc.subtotal == 153.00

    def test_line_item_calculation_negative_quantity(self):
        with pytest.raises(ValueError):
            LineItemCalculation.calculate("CP-075", -1, 8.50)

    def test_quote_totals(self):
        items = [
            LineItemCalculation.calculate("CP-075", 18, 8.50),
            LineItemCalculation.calculate("SV-075", 1, 24.00),
        ]
        totals = QuoteTotals.from_items(items, labor_hours=1, labor_rate=120.00)
        assert totals.line_item_subtotal == 177.00
        assert totals.labor_total == 120.00
        assert totals.total == 297.00


class TestTools(TestBase):
    async def test_get_price_list(self, seeded_session):
        result = await execute_tool(
            seeded_session,
            "get_price_list",
            {"items": [{"category": "copper_pipe", "specification": "3/4 inch"}]},
        )
        assert result["success"] is True
        assert result["count"] >= 1
        assert any(item["sku"] == "CP-075" for item in result["items"])

    async def test_calculate_line_item(self, seeded_session):
        result = await execute_tool(
            seeded_session,
            "calculate_line_item",
            {"sku": "CP-075", "quantity": 18, "unit_price": 8.50},
        )
        assert result["success"] is True
        assert result["subtotal"] == 153.00

    async def test_create_draft_quote(self, seeded_session):
        result = await execute_tool(
            seeded_session,
            "create_draft_quote",
            {
                "customer_name": "Test",
                "line_items": [
                    {"sku": "CP-075", "quantity": 18, "unit_price": 8.50},
                ],
            },
        )
        assert result["success"] is True
        assert result["quote_number"].startswith("TQ-")
        assert result["total"] == 153.00

    async def test_confirm_and_send(self, seeded_session):
        create_result = await execute_tool(
            seeded_session,
            "create_draft_quote",
            {
                "line_items": [
                    {"sku": "CP-075", "quantity": 10, "unit_price": 8.50},
                ],
            },
        )
        quote_id = create_result["quote_id"]

        result = await execute_tool(
            seeded_session,
            "confirm_and_send",
            {"quote_id": quote_id},
        )
        assert result["success"] is True
        assert result["status"] == "SENT"

    async def test_unknown_tool(self, seeded_session):
        result = await execute_tool(
            seeded_session,
            "nonexistent_tool",
            {},
        )
        assert result["success"] is False
        assert "Unknown tool" in result["error"]