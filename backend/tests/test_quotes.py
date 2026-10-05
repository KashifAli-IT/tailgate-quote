import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.db.database import Base
from app.services.quote_service import QuoteService
from app.services.evidence_service import EvidenceService
from app.db.seed import SEED_CATALOG
from app.models.catalog_item import CatalogItem


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


class TestQuotes(TestBase):
    async def test_create_quote(self, seeded_session):
        service = QuoteService(seeded_session)
        quote = await service.create_quote(
            customer_name="John",
            job_address="123 Main St",
            line_items=[
                {"sku": "CP-075", "quantity": 18, "unit_price": 8.50},
                {"sku": "SV-075", "quantity": 1, "unit_price": 24.00},
            ],
            labor_hours=1,
            labor_rate=120.00,
        )
        assert quote.status == "DRAFT"
        assert len(quote.items) == 2
        assert quote.quote_number.startswith("TQ-")

    async def test_confirm_and_send(self, seeded_session):
        service = QuoteService(seeded_session)
        quote = await service.create_quote(
            line_items=[{"sku": "CP-075", "quantity": 10, "unit_price": 8.50}],
        )
        assert quote.status == "DRAFT"

        sent_quote = await service.confirm_and_send(quote.id, confirmed_by="John")
        assert sent_quote.status == "SENT"
        assert sent_quote.sent_at is not None

    async def test_confirm_and_send_not_draft(self, seeded_session):
        service = QuoteService(seeded_session)
        quote = await service.create_quote(
            line_items=[{"sku": "CP-075", "quantity": 10, "unit_price": 8.50}],
        )
        await service.confirm_and_send(quote.id)

        with pytest.raises(ValueError, match="cannot send"):
            await service.confirm_and_send(quote.id)

    async def test_recalculate_totals(self, seeded_session):
        service = QuoteService(seeded_session)
        quote = await service.create_quote(
            line_items=[
                {"sku": "CP-075", "quantity": 18, "unit_price": 8.50},
            ],
        )
        assert quote.total == 153.00

        updated = await service.recalculate_totals(quote.id)
        assert updated.total == 153.00


class TestEvidence(TestBase):
    async def test_add_and_get_evidence(self, seeded_session):
        quote_service = QuoteService(seeded_session)
        quote = await quote_service.create_quote(
            line_items=[{"sku": "CP-075", "quantity": 10, "unit_price": 8.50}],
        )

        evidence_service = EvidenceService(seeded_session)
        await evidence_service.add_evidence(
            quote_id=quote.id,
            field_name="quantity",
            field_value="18",
            source_type="transcript",
            source_text="about eighteen feet",
        )

        result = await evidence_service.get_for_quote(quote.id)
        assert len(result.items) == 1
        assert result.items[0].field_name == "quantity"
        assert result.items[0].source_type == "transcript"