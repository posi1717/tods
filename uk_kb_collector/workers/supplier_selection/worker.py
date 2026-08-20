"""Independent reasoning worker for Supplier Selection."""

from pathlib import Path

from ..base import ReasoningWorker


class SupplierSelectionWorker(ReasoningWorker):
    pass


def create_worker() -> SupplierSelectionWorker:
    return SupplierSelectionWorker(Path(__file__).parent)
