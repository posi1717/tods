"""Specialist governance worker for MOUUK-0005 (Procurement Policy Notes)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0005Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Procurement Policy Notes."""


def create_worker() -> MOUUK0005Worker:
    return MOUUK0005Worker(Path(__file__).parent)
