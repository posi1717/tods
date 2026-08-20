"""Independent reasoning worker for Procurement Policy Notes (PPN)."""

from pathlib import Path

from ..base import ReasoningWorker


class PpnWorker(ReasoningWorker):
    pass


def create_worker() -> PpnWorker:
    return PpnWorker(Path(__file__).parent)
