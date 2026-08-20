"""Independent reasoning worker for Sustainability & Carbon."""

from pathlib import Path

from ..base import ReasoningWorker


class CarbonWorker(ReasoningWorker):
    pass


def create_worker() -> CarbonWorker:
    return CarbonWorker(Path(__file__).parent)
