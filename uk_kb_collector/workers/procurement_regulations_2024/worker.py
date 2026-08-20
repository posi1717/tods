"""Independent reasoning worker for Procurement Regulations 2024."""

from pathlib import Path

from ..base import ReasoningWorker


class ProcurementRegulations2024Worker(ReasoningWorker):
    pass


def create_worker() -> ProcurementRegulations2024Worker:
    return ProcurementRegulations2024Worker(Path(__file__).parent)
