"""Legacy Procurement Regulations specialist plugin."""

from .worker import LegacyProcurementRegulationsWorker, create_worker

__all__ = ["LegacyProcurementRegulationsWorker", "create_worker"]
