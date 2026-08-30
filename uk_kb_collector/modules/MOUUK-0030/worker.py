"""Specialist worker for MOUUK-0030 (Conflicts of Interest)."""

from pathlib import Path
from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0030Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0030Worker:
    return MOUUK0030Worker(Path(__file__).parent)
