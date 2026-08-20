"""Version metadata helpers for governance evidence lifecycle."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VersionMarker:
    module_code: str
    version: int


class VersioningService:
    def next_version(self, existing_versions: list[int]) -> int:
        return (max(existing_versions) if existing_versions else 0) + 1
