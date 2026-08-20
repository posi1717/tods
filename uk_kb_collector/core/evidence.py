"""Evidence bundle types for reasoning handoff and traceability."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceItem:
    module_code: str
    evidence_id: str
    text: str
    source_url: str
    document_sha256: str


@dataclass(frozen=True)
class ClaimRecord:
    module_code: str
    claim_id: str
    claim_text: str
    evidence_ids: tuple[str, ...]
    needs_review: bool


@dataclass(frozen=True)
class EvidenceBundle:
    items: tuple[EvidenceItem, ...]

    def by_id(self) -> dict[str, EvidenceItem]:
        return {item.evidence_id: item for item in self.items}
