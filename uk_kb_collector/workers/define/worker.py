"""Independent reasoning worker for Define."""

from pathlib import Path

from ..base import ReasoningWorker


class DefineWorker(ReasoningWorker):
    pass


def create_worker() -> DefineWorker:
    return DefineWorker(Path(__file__).parent)
