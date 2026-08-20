"""Specialist governance worker for MOUUK-0024 (Temporal and Version Intelligence)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0024Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Temporal and Version Intelligence."""


def create_worker() -> MOUUK0024Worker:
    return MOUUK0024Worker(Path(__file__).parent)
