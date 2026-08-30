from dataclasses import dataclass, field
from threading import RLock


@dataclass
class Registry:
    documents: dict[str, object] = field(default_factory=dict)
    versions: dict[str, object] = field(default_factory=dict)
    _lock: RLock = field(default_factory=RLock, repr=False)

    def add_document(self, document_id: str, document: object) -> None:
        with self._lock:
            self.documents.setdefault(document_id, document)

    def add_version(self, version_id: str, version: object) -> None:
        with self._lock:
            if version_id in self.versions and self.versions[version_id] != version:
                raise ValueError("document versions are immutable")
            self.versions[version_id] = version

    def has_hash(self, sha256: str) -> bool:
        return any(getattr(version, "sha256", None) == sha256 for version in self.versions.values())
