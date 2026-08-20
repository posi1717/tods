"""Discovery and dispatch for the 26 independent MOUUK plugins."""

from __future__ import annotations

import importlib

from .base import ReasoningRequest, ReasoningResponse, ReasoningWorker
from ..core.module_registry import ModuleRegistry


class PluginManager:
    def __init__(self) -> None:
        self.registry = ModuleRegistry.load()
        self._workers: dict[str, ReasoningWorker] = {}

    def load(self, identifier: str) -> ReasoningWorker:
        definition = self.registry.get(identifier)
        if definition.code not in self._workers:
            module = importlib.import_module(f"uk_kb_collector.workers.{definition.slug}.worker")
            worker = module.create_worker()
            if worker.module_code != definition.code:
                raise ValueError(f"plugin identity mismatch for {definition.slug}")
            self._workers[definition.code] = worker
        return self._workers[definition.code]

    def invoke(self, identifier: str, request: ReasoningRequest) -> ReasoningResponse:
        return self.load(identifier).reason(request)

    def load_all(self) -> list[ReasoningWorker]:
        return [self.load(definition.code) for definition in self.registry]
