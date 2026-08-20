from pathlib import Path
from datetime import date

from uk_kb_collector.core import (
    ClaimRecord,
    DocumentRecord,
    DocumentRegistry,
    EvidenceBundle,
    EvidenceItem,
    ModuleRegistry,
    ProvenanceEnvelope,
)
from uk_kb_collector.workers import PluginManager, ReasoningRequest


def test_26_permanent_module_directories_have_required_structure():
    modules_root = Path(__file__).parents[1] / "uk_kb_collector" / "modules"
    required_files = {"worker.py", "module.yaml", "sources.yaml", "rules.yaml", "taxonomy.yaml"}

    module_dirs = sorted(path for path in modules_root.iterdir() if path.is_dir() and path.name.startswith("MOUUK-"))
    assert len(module_dirs) == 26

    for module_dir in module_dirs:
        names = {path.name for path in module_dir.iterdir()}
        assert required_files.issubset(names)
        assert "tests" in names
        assert "data" in names


def test_module_ids_remain_stable_and_complete():
    registry = ModuleRegistry.load()
    assert [module.code for module in registry] == [f"MOUUK-{number:04d}" for number in range(1, 27)]


def test_document_registry_retains_required_metadata_fields():
    registry = DocumentRegistry()
    record = DocumentRecord(
        module_code="MOUUK-0001",
        source_url="https://www.legislation.gov.uk/ukpga/2023/54/contents",
        publisher="The National Archives",
        publication_date=date(2023, 10, 26),
        checked_date=date(2026, 8, 19),
        version=1,
        sha256="a" * 64,
    )
    registry.add(record)
    stored = registry.list()[0]

    assert stored.source_url
    assert stored.publisher
    assert stored.checked_date == date(2026, 8, 19)
    assert stored.version == 1
    assert len(stored.sha256) == 64


def test_claims_are_traceable_to_evidence_items():
    evidence = EvidenceItem(
        module_code="MOUUK-0005",
        evidence_id="EV-1",
        text="PPN reference text",
        source_url="https://www.gov.uk/government/publications/example",
        document_sha256="b" * 64,
    )
    bundle = EvidenceBundle(items=(evidence,))
    claim = ClaimRecord(
        module_code="MOUUK-0005",
        claim_id="CL-1",
        claim_text="The document is a procurement policy note.",
        evidence_ids=("EV-1",),
        needs_review=False,
    )

    assert set(claim.evidence_ids).issubset(bundle.by_id().keys())


def test_ambiguous_inputs_default_to_needs_review():
    response = PluginManager().invoke("MOUUK-0015", ReasoningRequest("Classify this"))
    assert response.needs_review is True
    assert response.confidence == 0.0


def test_provenance_envelope_matches_document_lineage_fields():
    envelope = ProvenanceEnvelope(
        module_code="MOUUK-0026",
        source_url="https://www.gov.uk/example.pdf",
        publisher="Cabinet Office",
        publication_date=None,
        checked_date=date(2026, 8, 19),
        version=3,
        sha256="c" * 64,
    )

    assert envelope.module_code == "MOUUK-0026"
    assert envelope.version == 3
    assert len(envelope.sha256) == 64
