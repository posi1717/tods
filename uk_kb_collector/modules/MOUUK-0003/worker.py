"""Specialist governance worker for MOUUK-0003 (Legacy Procurement Regulations)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0003Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Legacy Procurement Regulations."""


def create_worker() -> MOUUK0003Worker:
    return MOUUK0003Worker(Path(__file__).parent)
