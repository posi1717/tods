"""Specialist governance worker for MOUUK-0001 (Procurement Act 2023)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0001Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Procurement Act 2023."""


def create_worker() -> MOUUK0001Worker:
    return MOUUK0001Worker(Path(__file__).parent)
