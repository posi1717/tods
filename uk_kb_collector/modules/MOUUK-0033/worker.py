"""Specialist worker for MOUUK-0033 (Economic and Financial Standing)."""

from pathlib import Path
from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0033Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0033Worker:
    return MOUUK0033Worker(Path(__file__).parent)
