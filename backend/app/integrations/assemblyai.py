from typing import Optional

from ..config import settings


class AssemblyAIIntegration:
    """Integration layer for AssemblyAI Voice Agent API."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or settings.assemblyai_api_key
        self.agent_url = settings.assemblyai_agent_url

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def get_headers(self) -> dict:
        if not self.api_key:
            return {}
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_tool_definitions(self) -> list:
        from ..schemas.tools import ALL_TOOLS
        return ALL_TOOLS