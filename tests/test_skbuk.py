from pathlib import Path

from uk_kb_collector.models import DocumentRecord
from uk_kb_collector.skbuk import sync_records


def test_skbuk_owns_pdf_and_mouuk_receives_reference_only(tmp_path: Path):
    source_dir = tmp_path / "01_Legislation" / "Procurement_Act_2023"
    source_dir.mkdir(parents=True)
    pdf = source_dir / "2023__UK Government__Procurement Act__v1.pdf"
    pdf.write_bytes(b"%PDF-1.7\nraw-reference")

    record = DocumentRecord(
        document_id="doc-001",
        title="Procurement Act 2023",
        filename=pdf.name,
        category="01_Legislation/Procurement_Act_2023",
        source_url="https://www.legislation.gov.uk/ukpga/2023/54/contents",
        landing_page_url="https://www.legislation.gov.uk/ukpga/2023/54/contents",
        publisher="UK Parliament / legislation.gov.uk",
        document_type="legislation",
        legislation_or_policy_reference="Procurement Act 2023",
        publication_date="2023-10-26",
        last_checked_at="2026-08-21T00:00:00+00:00",
        downloaded_at="2026-08-21T00:00:00+00:00",
        file_size_bytes=pdf.stat().st_size,
        sha256="",
        http_last_modified="",
        etag="",
        status="active",
        relevance_tags=[],
    )

    # The fixture's hash is not used for the routing assertion; production records
    # always carry the validated collector SHA-256.
    result = sync_records(tmp_path, [record])
    assert result["documents_synced"] == 1

    stored = tmp_path / "SKBUK" / "documents" / "doc-001" / pdf.name
    manifest = tmp_path / "SKBUK" / "delivery" / "MOUUK" / "MOUUK-0001.json"

    assert stored.exists()
    assert manifest.exists()
    assert not (tmp_path / "modules" / "MOUUK-0001" / "references" / pdf.name).exists()

    payload = manifest.read_text(encoding="utf-8")
    assert record.source_url in payload
    assert "SKBUK/documents" in payload
