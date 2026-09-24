"""Compatibility access to the canonical MOUUK module catalogue.

The source of truth is ``uk_kb_collector/modules.yaml`` and is loaded through
``uk_kb_collector.core.module_registry.ModuleRegistry``.  This adapter keeps the
older ``MOUUKRegistry.get_module_info`` API without maintaining a second,
incomplete copy of module metadata.
"""

from __future__ import annotations

from uk_kb_collector.core.module_registry import ModuleRegistry


class MOUUKRegistry:
    """Expose all 34 stable MOUUK definitions through the legacy interface."""

    def __init__(self) -> None:
        self._registry = ModuleRegistry.load()
        self.modules = {
            module.code: {
                "code": module.code,
                "slug": module.slug,
                "name": module.name,
                "layer": module.layer,
                "kind": module.kind,
                "parent": module.parent,
            }
            for module in self._registry
        }

    @staticmethod
    def _normalise(identifier: str) -> str:
        if identifier.startswith("MOUUK_"):
            return identifier.replace("MOUUK_", "MOUUK-", 1)
        return identifier

    def get_module_info(self, identifier: str) -> dict[str, str | None]:
        """Return a stable module definition or raise for an unknown identifier.

        Both canonical codes (``MOUUK-0001``) and legacy underscore codes
        (``MOUUK_0001``) are accepted. Slugs are also supported by the canonical
        registry. Unknown values must not silently become "General Compliance"
        because that would hide routing and governance errors.
        """
        module = self._registry.get(self._normalise(identifier))
        return {
            "code": module.code,
            "slug": module.slug,
            "name": module.name,
            "layer": module.layer,
            "kind": module.kind,
            "parent": module.parent,
        }

    def list_modules(self) -> tuple[dict[str, str | None], ...]:
        """Return all modules in canonical catalogue order."""
        return tuple(self.modules.values())
