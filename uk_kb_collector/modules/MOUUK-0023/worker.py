"""Specialist governance worker for MOUUK-0023 (Source Authority)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0023Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Source Authority."""


def create_worker() -> MOUUK0023Worker:
    return MOUUK0023Worker(Path(__file__).parent)
