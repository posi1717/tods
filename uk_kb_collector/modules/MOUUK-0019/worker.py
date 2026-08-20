"""Specialist governance worker for MOUUK-0019 (Sustainability and Carbon)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0019Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Sustainability and Carbon."""


def create_worker() -> MOUUK0019Worker:
    return MOUUK0019Worker(Path(__file__).parent)
