"""Specialist governance worker for MOUUK-0006 (National Procurement Policy Statement)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0006Worker(ReasoningWorker):
    """Module-specialist worker scaffold for National Procurement Policy Statement."""


def create_worker() -> MOUUK0006Worker:
    return MOUUK0006Worker(Path(__file__).parent)
