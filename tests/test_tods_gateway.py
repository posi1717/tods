from datetime import datetime, timezone
from hashlib import sha256

from tods_gateway import (
    AuthorityLevel,
    EvidenceBundle,
    EvidenceItem,
    KnowledgeClaim,
    MOUUK_MODULES,
    calibrate_claim,
)


def test_registry_contains_all_34_modules() -> None:
    assert len(MOUUK_MODULES) == 34
    assert MOUUK_MODULES[0].module_id == "MOUUK-0001"
    assert MOUUK_MODULES[-1].module_id == "MOUUK-0034"


def test_calibration_passes_for_grounded_claim() -> None:
    text = "Official procurement guidance applies to the stated case."
    item = EvidenceItem(
        document_id="govuk-example-001",
        version_id="v01",
        source_url="https://www.gov.uk/example",
        publisher="GOV.UK",
        authority=AuthorityLevel.OFFICIAL_GUIDANCE,
        title="Example official procurement guidance",
        retrieved_at=datetime.now(timezone.utc),
        excerpt=text,
        passage_reference="Section 1",
        checksum_sha256=sha256(text.encode("utf-8")).hexdigest(),
    )
    bundle = EvidenceBundle(query="example procurement requirement", items=[item])
    claim = KnowledgeClaim(
        module_id="MOUUK-0001",
        statement="The requirement should be assessed using the cited official guidance.",
        evidence_document_ids=[item.document_id],
        confidence=0.85,
        evidence_fingerprint=bundle.evidence_fingerprint,
    )

    result = calibrate_claim(claim, bundle)

    assert result.passed is True
    assert result.status.value == "calibrated"


def test_calibration_blocks_missing_evidence_reference() -> None:
    text = "Official procurement guidance applies to the stated case."
    item = EvidenceItem(
        document_id="govuk-example-002",
        version_id="v01",
        source_url="https://www.gov.uk/example",
        publisher="GOV.UK",
        authority=AuthorityLevel.OFFICIAL_GUIDANCE,
        title="Example official procurement guidance",
        retrieved_at=datetime.now(timezone.utc),
        excerpt=text,
        checksum_sha256=sha256(text.encode("utf-8")).hexdigest(),
    )
    bundle = EvidenceBundle(query="example procurement requirement", items=[item])
    claim = KnowledgeClaim(
        module_id="MOUUK-0001",
        statement="This claim deliberately cites a document that is absent from the bundle.",
        evidence_document_ids=["missing-document"],
        confidence=0.90,
        evidence_fingerprint=bundle.evidence_fingerprint,
    )

    result = calibrate_claim(claim, bundle)

    assert result.passed is False
    assert result.status.value == "blocked"
    assert any("Missing cited evidence" in reason for reason in result.reasons)

