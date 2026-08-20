"""Independent reasoning worker for Framework Agreements."""

from pathlib import Path

from ..base import ReasoningWorker


class FrameworksWorker(ReasoningWorker):
    pass


def create_worker() -> FrameworksWorker:
    return FrameworksWorker(Path(__file__).parent)
