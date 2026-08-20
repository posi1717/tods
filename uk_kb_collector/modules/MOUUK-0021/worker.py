"""Specialist governance worker for MOUUK-0021 (Security and National Security)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0021Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Security and National Security."""


def create_worker() -> MOUUK0021Worker:
    return MOUUK0021Worker(Path(__file__).parent)
