from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.database import get_db
from ...schemas.tools import (
    ALL_TOOLS,
    ToolCallRequest,
    ToolResultResponse,
)
from ...tools import execute_tool

router = APIRouter(prefix="/api/v1", tags=["voice"])


@router.get("/tools", response_model=list)
async def list_tools():
    return ALL_TOOLS


@router.post("/tools/execute", response_model=ToolResultResponse)
async def execute_tool_endpoint(
    payload: ToolCallRequest,
    session: AsyncSession = Depends(get_db),
):
    result = await execute_tool(
        session,
        payload.tool_name,
        payload.arguments,
    )
    return ToolResultResponse(
        tool=payload.tool_name,
        success=result.get("success", True),
        result=result,
    )