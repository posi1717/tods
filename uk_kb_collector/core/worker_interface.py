"""Shared worker interface for governance modules."""

from __future__ import annotations

from typing import Protocol


class GovernanceWorker(Protocol):
    module_code: str

    def healthcheck(self) -> str: ...
