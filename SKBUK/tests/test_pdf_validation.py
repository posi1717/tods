from pathlib import Path
import pytest
from skbuk.services.validator import validate_pdf


def test_html_and_bad_magic_are_rejected(tmp_path: Path):
    path = tmp_path / "bad.pdf"
    path.write_bytes(b"<html>error</html>")
    with pytest.raises(ValueError):
        validate_pdf(path, "application/pdf", 1000)


def test_valid_pdf_magic_is_accepted(tmp_path: Path):
    path = tmp_path / "good.pdf"
    path.write_bytes(b"%PDF-1.7\n")
    validate_pdf(path, "application/pdf", 1000)
