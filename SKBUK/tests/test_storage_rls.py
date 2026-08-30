from pathlib import Path


def test_storage_migration_creates_private_buckets_without_public_policies():
    text = Path("sql/002_skbuk_storage_rls.sql").read_text(encoding="utf-8")
    assert "public)" in text
    assert "anonymous/browser access" in text
    assert "create policy" not in text.lower()
    assert text.lower().count("enable row level security") == 12
