"""Specialist governance worker for MOUUK-0008 (Define)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0008Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Define."""


def create_worker() -> MOUUK0008Worker:
    return MOUUK0008Worker(Path(__file__).parent)
