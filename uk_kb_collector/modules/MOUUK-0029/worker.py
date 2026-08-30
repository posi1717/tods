"""Specialist worker for MOUUK-0029 (Below-threshold and Covered Procurement)."""

from pathlib import Path
from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0029Worker(ReasoningWorker):
    pass


def create_worker() -> MOUUK0029Worker:
    return MOUUK0029Worker(Path(__file__).parent)
