"""Independent reasoning worker for Temporal & Version Intelligence."""

from pathlib import Path

from ..base import ReasoningWorker


class TemporalEngineWorker(ReasoningWorker):
    pass


def create_worker() -> TemporalEngineWorker:
    return TemporalEngineWorker(Path(__file__).parent)
