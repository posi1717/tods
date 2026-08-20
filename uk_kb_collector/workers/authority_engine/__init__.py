"""Source Authority specialist plugin."""

from .worker import AuthorityEngineWorker, create_worker

__all__ = ["AuthorityEngineWorker", "create_worker"]
