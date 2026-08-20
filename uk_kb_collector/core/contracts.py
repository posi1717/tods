"""Contracts shared by orchestrator services and workers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class WorkItem:
    module_code: str
    source_url: str
    context: dict[str, Any] = field(default_factory=dict)


class Worker(Protocol):
    module_code: str

    def collect(self) -> list[WorkItem]: ...
