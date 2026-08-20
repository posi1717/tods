"""Specialist governance worker for MOUUK-0007 (Plan)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0007Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Plan."""


def create_worker() -> MOUUK0007Worker:
    return MOUUK0007Worker(Path(__file__).parent)
