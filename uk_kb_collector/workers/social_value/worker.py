"""Independent reasoning worker for Social Value."""

from pathlib import Path

from ..base import ReasoningWorker


class SocialValueWorker(ReasoningWorker):
    pass


def create_worker() -> SocialValueWorker:
    return SocialValueWorker(Path(__file__).parent)
