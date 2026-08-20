"""Orchestrates governance intelligence runs over registered modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .module_registry import ModuleRegistry
from .worker_interface import GovernanceWorker


@dataclass(frozen=True)
class OrchestrationPlan:
    module_codes: tuple[str, ...]


class GovernanceOrchestrator:
    def __init__(self, registry: ModuleRegistry | None = None) -> None:
        self.registry = registry or ModuleRegistry.load()

    def plan(self, module_codes: Iterable[str] | None = None) -> OrchestrationPlan:
        if module_codes is None:
            selected = tuple(module.code for module in self.registry)
        else:
            selected = tuple(self.registry.get(code).code for code in module_codes)
        return OrchestrationPlan(module_codes=selected)

    def run(self, workers: Iterable[GovernanceWorker], module_codes: Iterable[str] | None = None) -> dict[str, str]:
        plan = self.plan(module_codes)
        results: dict[str, str] = {}
        by_code = {worker.module_code: worker for worker in workers}
        for code in plan.module_codes:
            worker = by_code.get(code)
            if worker is None:
                results[code] = "not_loaded"
                continue
            results[code] = worker.healthcheck()
        return results
