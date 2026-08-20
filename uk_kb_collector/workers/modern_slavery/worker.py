"""Independent reasoning worker for Modern Slavery & Responsible Supply Chain."""

from pathlib import Path

from ..base import ReasoningWorker


class ModernSlaveryWorker(ReasoningWorker):
    pass


def create_worker() -> ModernSlaveryWorker:
    return ModernSlaveryWorker(Path(__file__).parent)
