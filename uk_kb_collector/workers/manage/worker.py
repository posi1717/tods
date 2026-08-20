"""Independent reasoning worker for Manage."""

from pathlib import Path

from ..base import ReasoningWorker


class ManageWorker(ReasoningWorker):
    pass


def create_worker() -> ManageWorker:
    return ManageWorker(Path(__file__).parent)
