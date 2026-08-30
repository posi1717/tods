import hashlib
from pathlib import Path
from pypdf import PdfReader
from skbuk.models.source_excerpt import SourceExcerpt
from skbuk.utils.timestamps import utc_now


def extract_pdf(path: Path, document_version_id: str, confidence: float = 1.0) -> list[SourceExcerpt]:
    reader = PdfReader(str(path))
    excerpts: list[SourceExcerpt] = []
    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            continue
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        excerpts.append(SourceExcerpt(
            excerpt_id=f"exc_{document_version_id}_{index}", document_version_id=document_version_id,
            page_start=index, page_end=index, text=text, text_sha256=digest,
            extractor_name="pypdf", extractor_version="6", confidence=confidence, created_at=utc_now(),
        ))
    return excerpts
