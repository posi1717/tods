"""Specialist governance worker for MOUUK-0014 (Exclusion and Debarment)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0014Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Exclusion and Debarment."""


def create_worker() -> MOUUK0014Worker:
    return MOUUK0014Worker(Path(__file__).parent)
