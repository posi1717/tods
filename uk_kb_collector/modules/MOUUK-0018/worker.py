"""Specialist governance worker for MOUUK-0018 (Contract Management and Open Book)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0018Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Contract Management and Open Book."""


def create_worker() -> MOUUK0018Worker:
    return MOUUK0018Worker(Path(__file__).parent)
