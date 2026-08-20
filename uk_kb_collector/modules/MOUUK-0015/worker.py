"""Specialist governance worker for MOUUK-0015 (Transparency and Procurement Data)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0015Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Transparency and Procurement Data."""


def create_worker() -> MOUUK0015Worker:
    return MOUUK0015Worker(Path(__file__).parent)
