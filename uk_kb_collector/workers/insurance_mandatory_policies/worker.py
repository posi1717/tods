"""Worker for MOUUK-0034 Insurance and Mandatory Policies."""
from pathlib import Path
from ..base import ReasoningWorker


class MOUUK0034Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0034Worker:
    return MOUUK0034Worker(Path(__file__).parents[2] / "modules" / "MOUUK-0034")
