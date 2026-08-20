"""Specialist governance worker for MOUUK-0002 (Procurement Regulations 2024)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0002Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Procurement Regulations 2024."""


def create_worker() -> MOUUK0002Worker:
    return MOUUK0002Worker(Path(__file__).parent)
