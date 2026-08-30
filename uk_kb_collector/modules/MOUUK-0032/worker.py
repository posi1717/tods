"""Specialist worker for MOUUK-0032 (Devolved and Sector Regimes)."""

from pathlib import Path
from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0032Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0032Worker:
    return MOUUK0032Worker(Path(__file__).parent)
