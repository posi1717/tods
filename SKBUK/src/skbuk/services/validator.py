from pathlib import Path


def validate_pdf(path: Path, content_type: str, max_bytes: int) -> None:
    if path.stat().st_size > max_bytes:
        raise ValueError("download exceeds configured size limit")
    if content_type.split(";", 1)[0].strip().lower() != "application/pdf":
        raise ValueError("content is not application/pdf")
    with path.open("rb") as stream:
        if stream.read(5) != b"%PDF-":
            raise ValueError("file does not start with PDF magic bytes")


def validate_html(content_type: str) -> None:
    if content_type.split(";", 1)[0].strip().lower() not in {"text/html", "application/xhtml+xml"}:
        raise ValueError("content is not permitted official HTML")
