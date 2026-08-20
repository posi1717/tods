"""Procurement Policy Notes (PPN) specialist plugin."""

from .worker import PpnWorker, create_worker

__all__ = ["PpnWorker", "create_worker"]
