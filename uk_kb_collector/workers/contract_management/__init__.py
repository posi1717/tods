"""Contract Management & Open Book specialist plugin."""

from .worker import ContractManagementWorker, create_worker

__all__ = ["ContractManagementWorker", "create_worker"]
