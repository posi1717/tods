"""Provenance envelope types for source traceability."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ProvenanceEnvelope:
    module_code: str
    source_url: str
    publisher: str
    publication_date: date | None
    checked_date: date
    version: int
    sha256: str
