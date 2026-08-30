"""Worker for MOUUK-0033 Economic and Financial Standing."""
from pathlib import Path
from ..base import ReasoningWorker


class MOUUK0033Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0033Worker:
    return MOUUK0033Worker(Path(__file__).parents[2] / "modules" / "MOUUK-0033")
