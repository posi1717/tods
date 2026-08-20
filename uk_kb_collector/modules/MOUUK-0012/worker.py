"""Specialist governance worker for MOUUK-0012 (TOMs)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0012Worker(ReasoningWorker):
    """Module-specialist worker scaffold for TOMs."""


def create_worker() -> MOUUK0012Worker:
    return MOUUK0012Worker(Path(__file__).parent)
