from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.evidence import Evidence
from ..schemas.evidence import EvidenceSchema, EvidenceListResponse


class EvidenceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_evidence(
        self,
        quote_id: int,
        field_name: str,
        field_value: str,
        source_type: str,
        source_text: Optional[str] = None,
        source_location: Optional[str] = None,
    ) -> Evidence:
        evidence = Evidence(
            quote_id=quote_id,
            field_name=field_name,
            field_value=field_value,
            source_type=source_type,
            source_text=source_text,
            source_location=source_location,
        )
        self.session.add(evidence)
        await self.session.commit()
        await self.session.refresh(evidence)
        return evidence

    async def get_for_quote(self, quote_id: int) -> EvidenceListResponse:
        result = await self.session.execute(
            select(Evidence).where(Evidence.quote_id == quote_id)
        )
        items = list(result.scalars().all())
        return EvidenceListResponse(
            items=[EvidenceSchema.model_validate(i) for i in items]
        )