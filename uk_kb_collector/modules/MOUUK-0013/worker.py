"""Specialist governance worker for MOUUK-0013 (Supplier Selection)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0013Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Supplier Selection."""


def create_worker() -> MOUUK0013Worker:
    return MOUUK0013Worker(Path(__file__).parent)
