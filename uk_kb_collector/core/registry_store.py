"""In-memory governance registry facade for architecture scaffold."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegistryRecord:
    module_code: str
    source_url: str
    checksum: str | None = None


class RegistryStore:
    def __init__(self) -> None:
        self._records: list[RegistryRecord] = []

    def add(self, record: RegistryRecord) -> None:
        self._records.append(record)

    def list(self) -> list[RegistryRecord]:
        return list(self._records)
