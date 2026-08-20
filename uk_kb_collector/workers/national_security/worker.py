"""Independent reasoning worker for Security & National Security."""

from pathlib import Path

from ..base import ReasoningWorker


class NationalSecurityWorker(ReasoningWorker):
    pass


def create_worker() -> NationalSecurityWorker:
    return NationalSecurityWorker(Path(__file__).parent)
