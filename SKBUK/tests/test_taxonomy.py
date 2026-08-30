import pytest
from pydantic import ValidationError
from skbuk.models.document_version import DocumentVersion
from skbuk.models.inspection import ComplianceCheck


def test_official_version_cannot_use_bidder_bucket():
    with pytest.raises(ValidationError):
        DocumentVersion(version_id="v1", document_id="d1", run_id="r1", download_url="https://www.gov.uk/a.pdf", http_status=200, content_type="application/pdf", sha256="a" * 64, storage_bucket="tod-bidder", storage_path="02_BIDDER_EVIDENCE/o/B01/a.pdf", discovered_at="2026-01-01T00:00:00Z", downloaded_at="2026-01-01T00:00:01Z", is_binary_changed=True)


def test_not_specified_needs_no_evidence_but_affirmative_does():
    assert ComplianceCheck(check_id="c1", inspection_run_id="i1", outcome="not_specified").outcome == "not_specified"
    with pytest.raises(ValidationError):
        ComplianceCheck(check_id="c2", inspection_run_id="i1", outcome="compliant")
