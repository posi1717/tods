from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_data_governance_document_exists_and_names_both_schema_families():
    text = (ROOT / "docs/governance/DATA_GOVERNANCE_AND_LIFECYCLE.md").read_text(encoding="utf-8")

    assert "supabase/migrations/" in text
    assert "SKBUK/sql/" in text
    assert "must not both be described as one deployed schema" in text


def test_data_governance_requires_forward_only_reconciliation():
    text = (ROOT / "docs/governance/DATA_GOVERNANCE_AND_LIFECYCLE.md").read_text(encoding="utf-8")

    assert "new forward-only Supabase migrations" in text
    assert "existing migration files must not be rewritten" in text


def test_canonical_register_classifies_parallel_configuration_files():
    text = (ROOT / "docs/governance/CANONICAL_DOCUMENT_REGISTER.md").read_text(encoding="utf-8")

    assert "`sources.yml` | Proposed/reference" in text
    assert "`classification.yml` | Proposed/reference" in text
    assert "`supabase/migrations/**` | Canonical migration history" in text
