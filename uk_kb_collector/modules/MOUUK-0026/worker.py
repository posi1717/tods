"""Specialist governance worker for MOUUK-0026 (Evidence and Provenance)."""

from __future__ import annotations

from pathlib import Path

from uk_kb_collector.workers.base import ReasoningWorker


class MOUUK0026Worker(ReasoningWorker):
    """Module-specialist worker scaffold for Evidence and Provenance."""


def create_worker() -> MOUUK0026Worker:
    return MOUUK0026Worker(Path(__file__).parent)
