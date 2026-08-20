"""Independent reasoning worker for Procurement Act 2023."""

from pathlib import Path

from ..base import ReasoningWorker


class ProcurementAct2023Worker(ReasoningWorker):
    pass


def create_worker() -> ProcurementAct2023Worker:
    return ProcurementAct2023Worker(Path(__file__).parent)
