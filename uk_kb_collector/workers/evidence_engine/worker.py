"""Independent reasoning worker for Evidence & Provenance."""

from pathlib import Path

from ..base import ReasoningWorker


class EvidenceEngineWorker(ReasoningWorker):
    pass


def create_worker() -> EvidenceEngineWorker:
    return EvidenceEngineWorker(Path(__file__).parent)
