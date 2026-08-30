"""Specialist worker for MOUUK-0028 (Notices, Standstill and Remedies)."""

from pathlib import Path
from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0028Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0028Worker:
    return MOUUK0028Worker(Path(__file__).parent)
