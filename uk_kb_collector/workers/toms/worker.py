"""Independent reasoning worker for TOMs."""

from pathlib import Path

from ..base import ReasoningWorker


class TomsWorker(ReasoningWorker):
    pass


def create_worker() -> TomsWorker:
    return TomsWorker(Path(__file__).parent)
