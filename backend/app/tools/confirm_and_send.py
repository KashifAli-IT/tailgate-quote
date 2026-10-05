from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.quote_service import QuoteService
from ..schemas.tools import ConfirmAndSendRequest


async def confirm_and_send(session: AsyncSession, arguments: Dict[str, Any]) -> Dict[str, Any]:
    request = ConfirmAndSendRequest(**arguments)

    service = QuoteService(session)
    try:
        quote = await service.confirm_and_send(
            quote_id=request.quote_id,
            confirmed_by=request.confirmed_by,
        )
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
        }

    return {
        "success": True,
        "quote_id": quote.id,
        "quote_number": quote.quote_number,
        "status": quote.status,
        "sent_at": quote.sent_at.isoformat() if quote.sent_at else None,
        "total": quote.total,
    }