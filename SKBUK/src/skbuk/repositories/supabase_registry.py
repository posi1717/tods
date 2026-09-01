import httpx
from typing import Any

from skbuk.settings import Settings


class SupabaseRegistry:
    """Server-side adapter boundary; requires the service-role key at runtime."""

    def __init__(self, client: httpx.Client, base_url: str | None = None, service_role_key: str | None = None) -> None:
        self.client = client
        self.base_url = base_url.rstrip("/") if base_url else None
        self.service_role_key = service_role_key

    @classmethod
    def from_settings(cls, settings: Settings, client: httpx.Client | None = None) -> "SupabaseRegistry":
        if not settings.has_server_credentials:
            raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
        return cls(
            client or httpx.Client(timeout=settings.skbuk_timeout_seconds),
            settings.supabase_url,
            settings.supabase_service_role_key,
        )

    def _headers(self) -> dict[str, str]:
        if not self.base_url or not self.service_role_key:
            raise RuntimeError("Supabase server credentials are not configured")
        return {
            "apikey": self.service_role_key,
            "Authorization": "Bearer " + self.service_role_key,
        }

    def healthcheck(self) -> bool:
        """Verify registry access using a minimal read of a protected table."""
        if self.base_url is None:
            return False
        response = self.client.get(
            f"{self.base_url}/rest/v1/tod_ingestion_runs",
            params={"select": "run_id", "limit": "1"},
            headers=self._headers(),
        )
        return response.status_code == 200

    def insert(self, table: str, payload: dict[str, Any]) -> Any:
        if table.startswith("storage."):
            raise ValueError("registry adapter cannot write storage metadata tables")
        if self.base_url is None:
            raise RuntimeError("Supabase REST URL and service-role key are required for writes")
        response = self.client.post(
            f"{self.base_url}/rest/v1/{table}",
            json=payload,
            headers={**self._headers(), "Prefer": "return=representation"},
        )
        response.raise_for_status()
        return response.json()
