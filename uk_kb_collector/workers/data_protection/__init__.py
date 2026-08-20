"""Data Protection & Information Governance specialist plugin."""

from .worker import DataProtectionWorker, create_worker

__all__ = ["DataProtectionWorker", "create_worker"]
