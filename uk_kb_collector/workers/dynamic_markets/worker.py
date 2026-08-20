"""Independent reasoning worker for Dynamic Markets."""

from pathlib import Path

from ..base import ReasoningWorker


class DynamicMarketsWorker(ReasoningWorker):
    pass


def create_worker() -> DynamicMarketsWorker:
    return DynamicMarketsWorker(Path(__file__).parent)
