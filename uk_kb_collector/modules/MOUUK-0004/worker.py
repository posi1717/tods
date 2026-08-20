"""Specialist governance worker for MOUUK-0004 (Other Relevant Legislation)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0004Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Other Relevant Legislation."""


def create_worker() -> MOUUK0004Worker:
    return MOUUK0004Worker(Path(__file__).parent)
