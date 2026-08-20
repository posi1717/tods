"""Specialist governance worker for MOUUK-0020 (Modern Slavery and Responsible Supply Chain)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0020Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Modern Slavery and Responsible Supply Chain."""


def create_worker() -> MOUUK0020Worker:
    return MOUUK0020Worker(Path(__file__).parent)
