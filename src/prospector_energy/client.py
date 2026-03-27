"""HTTP client wrapper for the Prospector Labs API."""

import os
from typing import Any

import httpx

DEFAULT_API_URL = "https://prospector-platform-production.up.railway.app"


class ProspectorClient:
    """Async HTTP client for the Prospector Labs Energy Data API."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
        self.base_url = (
            base_url
            or os.environ.get("PROSPECTOR_API_URL")
            or DEFAULT_API_URL
        ).rstrip("/")
        self.api_key = api_key or os.environ.get("PROSPECTOR_API_KEY")
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        """Make a GET request, stripping None params."""
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        resp = await self._client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self._client.aclose()
