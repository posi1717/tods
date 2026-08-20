"""Specialist governance worker for MOUUK-0009 (Procure)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0009Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Procure."""


def create_worker() -> MOUUK0009Worker:
    return MOUUK0009Worker(Path(__file__).parent)
