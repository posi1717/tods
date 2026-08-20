"""Independent reasoning worker for National Procurement Policy Statement (NPPS)."""

from pathlib import Path

from ..base import ReasoningWorker


class NppsWorker(ReasoningWorker):
    pass


def create_worker() -> NppsWorker:
    return NppsWorker(Path(__file__).parent)
