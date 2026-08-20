"""Independent reasoning worker for Cross-Governance Relationships."""

from pathlib import Path

from ..base import ReasoningWorker


class RelationshipEngineWorker(ReasoningWorker):
    pass


def create_worker() -> RelationshipEngineWorker:
    return RelationshipEngineWorker(Path(__file__).parent)
