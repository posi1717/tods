"""Independent reasoning worker for Contract Management & Open Book."""

from pathlib import Path

from ..base import ReasoningWorker


class ContractManagementWorker(ReasoningWorker):
    pass


def create_worker() -> ContractManagementWorker:
    return ContractManagementWorker(Path(__file__).parent)
