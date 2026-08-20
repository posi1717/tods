from __future__ import annotations

import logging
from pathlib import Path

from pypdf import PdfReader

LOG = logging.getLogger(__name__)


def validate_pdf(path: Path, content_type: str, expected_size: int | None = None, max_bytes: int = 150_000_000) -> None:
    size = path.stat().st_size
    if size <= 0:
        raise ValueError("downloaded file is empty")
    if size > max_bytes:
        raise ValueError(f"PDF exceeds configured maximum size ({size} > {max_bytes})")
    with path.open("rb") as f:
        magic = f.read(5)
    if magic != b"%PDF-":
        raise ValueError("file does not start with PDF magic bytes")
    ct = (content_type or "").lower()
    if "application/pdf" not in ct and ct:
        raise ValueError(f"unexpected content type: {content_type}")
    if expected_size is not None and expected_size != size:
        LOG.warning("Content-Length %s differs from received bytes %s", expected_size, size)


def pdf_metadata(path: Path, probe_pages: int = 4, max_chars: int = 20_000) -> dict[str, str]:
    # Open the complete file because PDF xref/trailer structures are often near EOF.
    reader = PdfReader(str(path), strict=False)
    meta = reader.metadata or {}
    text_parts: list[str] = []
    try:
        full_reader = PdfReader(str(path), strict=False)
        for page in full_reader.pages[:probe_pages]:
            text_parts.append(page.extract_text() or "")
            if sum(map(len, text_parts)) >= max_chars:
                break
    except Exception as exc:
        LOG.warning("Could not extract PDF text from %s: %s", path, exc)
    text = "\n".join(text_parts)[:max_chars]
    return {
        "title": str(meta.get("/Title") or ""),
        "author": str(meta.get("/Author") or ""),
        "subject": str(meta.get("/Subject") or ""),
        "text": text,
    }
