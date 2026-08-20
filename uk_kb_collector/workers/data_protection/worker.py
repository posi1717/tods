"""Independent reasoning worker for Data Protection & Information Governance."""

from pathlib import Path

from ..base import ReasoningWorker


class DataProtectionWorker(ReasoningWorker):
    pass


def create_worker() -> DataProtectionWorker:
    return DataProtectionWorker(Path(__file__).parent)
