"""Independent reasoning worker for Exclusion & Debarment."""

from pathlib import Path

from ..base import ReasoningWorker


class ExclusionDebarmentWorker(ReasoningWorker):
    pass


def create_worker() -> ExclusionDebarmentWorker:
    return ExclusionDebarmentWorker(Path(__file__).parent)
