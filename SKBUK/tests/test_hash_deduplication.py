from pathlib import Path
from skbuk.services.hasher import sha256_file
from skbuk.services.registry import Registry
from skbuk.models.document_version import DocumentVersion


def test_duplicate_sha256_is_not_registered_twice(tmp_path: Path):
    path = tmp_path / "file.pdf"
    path.write_bytes(b"same")
    digest = sha256_file(path)
    registry = Registry()
    version = DocumentVersion(version_id="ver-1", document_id="doc-1", run_id="run-1", download_url="https://www.gov.uk/a.pdf", http_status=200, content_type="application/pdf", sha256=digest, storage_path="01_OFFICIAL_SOURCES/a.pdf", discovered_at="2026-01-01T00:00:00Z", downloaded_at="2026-01-01T00:00:01Z", is_binary_changed=True)
    registry.add_version(version.version_id, version)
    assert registry.has_hash(digest)
    assert registry.has_hash(digest)
