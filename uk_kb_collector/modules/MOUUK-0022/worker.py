"""Specialist governance worker for MOUUK-0022 (Data Protection and Information Governance)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0022Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Data Protection and Information Governance."""


def create_worker() -> MOUUK0022Worker:
    return MOUUK0022Worker(Path(__file__).parent)
