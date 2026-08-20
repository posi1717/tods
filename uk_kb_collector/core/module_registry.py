"""Validated registry for MOUUK collector modules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class ModuleDefinition:
    code: str
    slug: str
    name: str
    layer: str
    kind: str
    parent: str | None = None


class ModuleRegistry:
    """Load and query the canonical module catalogue."""

    def __init__(self, modules: list[ModuleDefinition]) -> None:
        self._by_code = {module.code: module for module in modules}
        self._by_slug = {module.slug: module for module in modules}
        if len(self._by_code) != len(modules) or len(self._by_slug) != len(modules):
            raise ValueError("module codes and slugs must be unique")
        for module in modules:
            if module.parent and module.parent not in self._by_code:
                raise ValueError(f"unknown parent {module.parent} for {module.code}")

    @classmethod
    def load(cls, path: Path | None = None) -> "ModuleRegistry":
        catalogue = path or Path(__file__).parents[1] / "modules.yaml"
        raw = yaml.safe_load(catalogue.read_text(encoding="utf-8"))
        return cls([ModuleDefinition(**item) for item in raw["modules"]])

    def get(self, identifier: str) -> ModuleDefinition:
        module = self._by_code.get(identifier) or self._by_slug.get(identifier)
        if module is None:
            raise KeyError(f"unknown module: {identifier}")
        return module

    def for_layer(self, layer: str) -> list[ModuleDefinition]:
        return [module for module in self._by_code.values() if module.layer == layer]

    def __iter__(self):
        return iter(self._by_code.values())
