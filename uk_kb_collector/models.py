from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


REGISTRY_FIELDS = [
    "document_id", "title", "filename", "category", "source_url", "landing_page_url",
    "publisher", "document_type", "legislation_or_policy_reference", "publication_date",
    "last_checked_at", "downloaded_at", "file_size_bytes", "sha256", "http_last_modified",
    "etag", "status", "relevance_tags", "notes", "supersedes", "superseded_by",
]


@dataclass
class DocumentRecord:
    document_id: str
    title: str
    filename: str
    category: str
    source_url: str
    landing_page_url: str
    publisher: str
    document_type: str
    legislation_or_policy_reference: str
    publication_date: str
    last_checked_at: str
    downloaded_at: str
    file_size_bytes: int
    sha256: str
    http_last_modified: str
    etag: str
    status: str
    relevance_tags: list[str] = field(default_factory=list)
    notes: str = ""
    supersedes: str = ""
    superseded_by: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
