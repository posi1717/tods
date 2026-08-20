from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

INVALID_WINDOWS = re.compile(r'[<>:"/\\|?*\x00-\x1F]')
RESERVED_WINDOWS = {
    "CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))
}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def slug_filename_part(value: str, fallback: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").strip()
    value = INVALID_WINDOWS.sub("_", value)
    value = re.sub(r"\s+", " ", value)
    value = value.rstrip(" .")
    if not value:
        value = fallback
    if value.upper() in RESERVED_WINDOWS:
        value = f"_{value}"
    return value[:180]


def build_filename(publication_date: str, publisher: str, title: str, version: int) -> str:
    date = publication_date if re.fullmatch(r"\d{4}-\d{2}-\d{2}", publication_date or "") else "undated"
    pub = slug_filename_part(publisher, "unknown-publisher")
    ttl = slug_filename_part(title, "untitled-document")
    return f"{date}__{pub}__{ttl}__v{version}.pdf"


def version_from_filename(filename: str) -> int:
    m = re.search(r"__v(\d+)\.pdf$", filename, re.I)
    return int(m.group(1)) if m else 1


def next_version(filenames: list[str]) -> int:
    return max((version_from_filename(x) for x in filenames), default=0) + 1


def document_id(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]


def version_document_id(url: str, sha256: str) -> str:
    return f"{document_id(url)}-{sha256[:12]}"


def allowed_host(url: str, allowed_domains: tuple[str, ...]) -> bool:
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    for pattern in allowed_domains:
        p = pattern.lower().lstrip("*." )
        if host == p or host.endswith("." + p):
            return True
    return False


def is_pdf_content(content_type: str, first_bytes: bytes) -> bool:
    ct = (content_type or "").lower()
    return first_bytes.startswith(b"%PDF-") and ("application/pdf" in ct or ct == "")
