"""Persist collection provenance to the protected SKBUK registry."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Protocol


class RegistryWriter(Protocol):
    def insert(self, table: str, payload: dict[str, Any]) -> Any: ...


def _iso_now() -> str:
    return datetime.now(UTC).isoformat()


class ProvenanceWriter:
    """Writes append-only collection run events without exposing document bytes."""

    def __init__(self, registry: RegistryWriter) -> None:
        self.registry = registry
        self.run_id: str | None = None

    def start(self) -> None:
        response = self.registry.insert("tod_ingestion_runs", {
            "started_at": _iso_now(),
            "status": "running",
        })
        self.run_id = response[0]["run_id"]

    def accepted_document(self, source_id: str, source_url: str, sha256: str, storage_path: str) -> None:
        if self.run_id is None:
            raise RuntimeError("provenance run has not started")
        self.registry.insert("tod_ingestion_events", {
            "run_id": self.run_id,
            "event_type": "document_collected",
            "payload": {
                "source_id": source_id,
                "source_url": source_url,
                "sha256": sha256,
                "storage_bucket": "tod-official",
                "storage_path": storage_path,
            },
        })

    def finish(self, status: str, summary: dict[str, int]) -> None:
        if self.run_id is None:
            return
        self.registry.insert("tod_ingestion_events", {
            "run_id": self.run_id,
            "event_type": "collection_finished",
            "payload": {"status": status, **summary},
        })
