"""Document registry contracts with provenance-critical metadata."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DocumentRecord:
    module_code: str
    source_url: str
    publisher: str
    publication_date: date | None
    checked_date: date
    version: int
    sha256: str


class DocumentRegistry:
    """In-memory registry scaffold for document lifecycle metadata."""

    def __init__(self) -> None:
        self._records: list[DocumentRecord] = []

    def add(self, record: DocumentRecord) -> None:
        self._records.append(record)

    def list(self) -> list[DocumentRecord]:
        return list(self._records)
