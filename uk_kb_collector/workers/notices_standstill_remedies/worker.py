"""Worker for MOUUK-0028 Notices, Standstill and Remedies."""
from pathlib import Path
from ..base import ReasoningWorker


class MOUUK0028Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0028Worker:
    return MOUUK0028Worker(Path(__file__).parents[2] / "modules" / "MOUUK-0028")
