"""Independent reasoning worker for Source Authority."""

from pathlib import Path

from ..base import ReasoningWorker


class AuthorityEngineWorker(ReasoningWorker):
    pass


def create_worker() -> AuthorityEngineWorker:
    return AuthorityEngineWorker(Path(__file__).parent)
