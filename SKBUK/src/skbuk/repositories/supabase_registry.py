from typing import Any


class SupabaseRegistry:
    """Server-side adapter boundary; requires the service-role key at runtime."""

    def __init__(self, client: Any) -> None:
        self.client = client

    def insert(self, table: str, payload: dict[str, Any]) -> Any:
        if table.startswith("storage."):
            raise ValueError("registry adapter cannot write storage metadata tables")
        return self.client.table(table).insert(payload).execute()
