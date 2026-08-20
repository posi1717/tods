"""Independent reasoning worker for Plan."""

from pathlib import Path

from ..base import ReasoningWorker


class PlanWorker(ReasoningWorker):
    pass


def create_worker() -> PlanWorker:
    return PlanWorker(Path(__file__).parent)
