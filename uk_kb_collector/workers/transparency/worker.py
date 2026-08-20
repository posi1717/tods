"""Independent reasoning worker for Transparency & Procurement Data."""

from pathlib import Path

from ..base import ReasoningWorker


class TransparencyWorker(ReasoningWorker):
    pass


def create_worker() -> TransparencyWorker:
    return TransparencyWorker(Path(__file__).parent)
