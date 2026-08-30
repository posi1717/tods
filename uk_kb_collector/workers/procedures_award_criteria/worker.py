"""Worker for MOUUK-0027 Procedures and Award Criteria."""
from pathlib import Path
from ..base import ReasoningWorker


class MOUUK0027Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0027Worker:
    return MOUUK0027Worker(Path(__file__).parents[2] / "modules" / "MOUUK-0027")
