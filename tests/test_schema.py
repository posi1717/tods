from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from uk_kb_collector.schema import Document, DocumentFamily, Rejection, RejectionReason, Run, RunStatus
from uk_kb_collector.schema_io import read_documents_csv, write_documents_csv


HASH = "a" * 64


def make_document() -> Document:
    return Document(
        document_id="doc_legislation_ukpga_2023_54",
        canonical_slug="procurement-act-2023",
        title="Procurement Act 2023",
        publisher="legislation.gov.uk",
        source_id="src_procurement_act_2023",
        document_family="primary-legislation",
        document_type="pdf",
        jurisdiction="UK",
        applicability="public-procurement",
        year=2023,
        language="en",
        authoritative_url="https://www.legislation.gov.uk/ukpga/2023/54/pdfs/ukpga_20230054_en.pdf",
        landing_url="https://www.legislation.gov.uk/ukpga/2023/54",
        canonical_page_url="https://www.legislation.gov.uk/ukpga/2023/54",
        first_seen_at="2026-08-21T14:00:00Z",
        first_seen_run_id="2026-08-21T140000Z",
        latest_seen_at="2026-08-21T14:00:00Z",
        latest_seen_run_id="2026-08-21T140000Z",
        latest_version_id="ver_doc_legislation_ukpga_2023_54_20260821T140000Z",
        latest_sha256=HASH,
        latest_download_url="https://www.legislation.gov.uk/ukpga/2023/54/pdfs/ukpga_20230054_en.pdf",
        latest_http_status=200,
        latest_content_type="application/pdf",
        latest_content_length=563451,
        latest_downloaded_at="2026-08-21T14:01:15Z",
        latest_file_name_original="ukpga_20230054_en.pdf",
        latest_file_path_current="data/documents/legislation-gov-uk/primary-legislation/2023/procurement-act-2023/current/original.pdf",
        latest_file_path_versioned="data/documents/legislation-gov-uk/primary-legislation/2023/procurement-act-2023/versions/2026-08-21T140115Z__sha256_aaaaaaaaaaaa.pdf",
        version_count=1,
        status="active",
    )


def test_document_csv_round_trip(tmp_path: Path):
    path = tmp_path / "documents.csv"
    write_documents_csv(path, [make_document()])
    loaded = read_documents_csv(path)
    assert loaded == [make_document()]
    assert path.read_bytes().startswith(b"\xef\xbb\xbf")


def test_schema_normalises_datetimes_to_utc():
    run = Run(
        run_id="2026-08-21T140000Z",
        started_at="2026-08-21T14:00:00+01:00",
        status=RunStatus.COMPLETED,
        app_version="0.1.0",
        source_count=1,
        discovered_count=1,
        downloaded_count=1,
        unchanged_count=0,
        rejected_count=0,
        error_count=0,
    )
    assert run.started_at == datetime(2026, 8, 21, 13, tzinfo=UTC)


def test_schema_rejects_non_official_url():
    with pytest.raises(ValidationError):
        Document.model_validate({**make_document().model_dump(), "landing_url": "https://example.com/source"})


def test_schema_rejects_path_traversal():
    with pytest.raises(ValidationError):
        Document.model_validate({**make_document().model_dump(), "latest_file_path_current": "data/documents/../secret.pdf"})


def test_rejection_reason_is_controlled():
    rejection = Rejection(
        rejection_id="rej_20260821_001",
        run_id="2026-08-21T140000Z",
        url="https://assets.publishing.service.gov.uk/file.pdf",
        host="assets.publishing.service.gov.uk",
        reason_code=RejectionReason.NOT_PDF,
        occurred_at="2026-08-21T14:00:00Z",
    )
    assert rejection.reason_code == "not_pdf"
    assert DocumentFamily.PRIMARY_LEGISLATION == "primary-legislation"
