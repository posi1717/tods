from pathlib import Path
from tempfile import TemporaryDirectory

from uk_kb_collector.categorize import classify
from uk_kb_collector.utils import allowed_host, build_filename, is_pdf_content, slug_filename_part


def test_filename_sanitisation():
    assert "/" not in slug_filename_part('bad:name/with*chars?', 'x')
    assert slug_filename_part("CON", "x") == "_CON"


def test_pdf_validation_magic_and_content_type():
    assert is_pdf_content("application/pdf", b"%PDF-1.7")
    assert not is_pdf_content("text/html", b"%PDF-1.7")
    assert not is_pdf_content("application/pdf", b"NOTPDF")


def test_host_allowlist():
    assert allowed_host("https://www.gov.uk/x", ("gov.uk",))
    assert allowed_host("https://assets.publishing.service.gov.uk/x", ("*.gov.uk",))
    assert allowed_host("https://www.legislation.gov.uk/ukpga/2023/54", ("legislation.gov.uk",))
    assert not allowed_host("https://example.com/x", ("gov.uk", "legislation.gov.uk"))


def test_categorisation():
    c = classify(
        "https://www.gov.uk/government/publications/ppn-001",
        "PPN 001: SME and VCSE procurement spend targets",
        {"title": "PPN 001", "subject": "procurement", "text": "SME VCSE procurement spend targets"},
        "procurement_policy_notes",
        {"SME_VCSE": ["SME", "VCSE"]},
    )
    assert c.category == "03_Procurement_Policy_Notes"
    assert "SME_VCSE" in c.tags


def test_filename_shape():
    name = build_filename("", "Cabinet Office", "A/B Guidance", 2)
    assert name == "undated__Cabinet Office__A_B Guidance__v2.pdf"
