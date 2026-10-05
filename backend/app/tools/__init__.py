from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from .get_price_list import get_price_list
from .calculate_line_item import calculate_line_item
from .create_draft_quote import create_draft_quote
from .confirm_and_send import confirm_and_send


TOOL_HANDLERS = {
    "get_price_list": get_price_list,
    "calculate_line_item": calculate_line_item,
    "create_draft_quote": create_draft_quote,
    "confirm_and_send": confirm_and_send,
}


async def execute_tool(
    session: AsyncSession,
    tool_name: str,
    arguments: Dict[str, Any],
) -> Dict[str, Any]:
    handler = TOOL_HANDLERS.get(tool_name)
    if handler is None:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
        }
    return await handler(session, arguments)