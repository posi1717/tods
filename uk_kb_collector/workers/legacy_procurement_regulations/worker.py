"""Independent reasoning worker for Legacy Procurement Regulations."""

from pathlib import Path

from ..base import ReasoningWorker


class LegacyProcurementRegulationsWorker(ReasoningWorker):
    pass


def create_worker() -> LegacyProcurementRegulationsWorker:
    return LegacyProcurementRegulationsWorker(Path(__file__).parent)
