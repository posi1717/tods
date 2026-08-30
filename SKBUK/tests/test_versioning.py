import pytest
from skbuk.models.document_version import DocumentVersion
from skbuk.services.registry import Registry


def version(version_id: str, digest: str) -> DocumentVersion:
    return DocumentVersion(version_id=version_id, document_id="doc-1", run_id="run-1", download_url="https://www.gov.uk/a.pdf", http_status=200, content_type="application/pdf", sha256=digest, storage_path=f"01_OFFICIAL_SOURCES/{version_id}.pdf", discovered_at="2026-01-01T00:00:00Z", downloaded_at="2026-01-01T00:00:01Z", is_binary_changed=True)


def test_changed_file_creates_immutable_version():
    registry = Registry()
    registry.add_version("ver-1", version("ver-1", "a" * 64))
    registry.add_version("ver-2", version("ver-2", "b" * 64))
    assert set(registry.versions) == {"ver-1", "ver-2"}
    with pytest.raises(ValueError):
        registry.add_version("ver-1", version("ver-1", "c" * 64))
