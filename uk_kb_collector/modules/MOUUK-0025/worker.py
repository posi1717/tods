"""Specialist governance worker for MOUUK-0025 (Cross-Governance Relationships)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0025Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Cross-Governance Relationships."""


def create_worker() -> MOUUK0025Worker:
    return MOUUK0025Worker(Path(__file__).parent)
