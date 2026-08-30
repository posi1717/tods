"""Specialist worker for MOUUK-0031 (SME, VCSE and Reserved Contracts)."""

from pathlib import Path
from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0031Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0031Worker:
    return MOUUK0031Worker(Path(__file__).parent)
