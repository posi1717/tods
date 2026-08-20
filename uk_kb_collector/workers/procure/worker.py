"""Independent reasoning worker for Procure."""

from pathlib import Path

from ..base import ReasoningWorker


class ProcureWorker(ReasoningWorker):
    pass


def create_worker() -> ProcureWorker:
    return ProcureWorker(Path(__file__).parent)
