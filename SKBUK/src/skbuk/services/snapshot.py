from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EvidenceSnapshot:
    inspection_run_id: str
    tender_id: str
    source_version_ids: tuple[str, ...]
    locked_at: datetime


def lock_snapshot(inspection_run_id: str, tender_id: str, version_ids: list[str], locked_at: datetime) -> EvidenceSnapshot:
    if not version_ids:
        raise ValueError("cannot lock an empty evidence snapshot")
    return EvidenceSnapshot(inspection_run_id, tender_id, tuple(dict.fromkeys(version_ids)), locked_at)
