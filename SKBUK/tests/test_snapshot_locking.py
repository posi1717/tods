import pytest
from datetime import UTC, datetime
from skbuk.services.snapshot import lock_snapshot


def test_snapshot_retains_exact_version_ids():
    snapshot = lock_snapshot("inspection-1", "tender-1", ["v1", "v2", "v1"], datetime.now(UTC))
    assert snapshot.source_version_ids == ("v1", "v2")


def test_empty_snapshot_cannot_lock():
    with pytest.raises(ValueError):
        lock_snapshot("inspection-1", "tender-1", [], datetime.now(UTC))
