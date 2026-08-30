"""SKBUK knowledge-store and governance gateway.

SKBUK owns document storage, provenance, audit/version metadata and delivery
manifests for the MOUUK expert modules. MOUUK modules never own the source
PDFs. This stage intentionally does not extract, chunk, embed or summarise.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .module_routing import route_modules
from .models import DocumentRecord
from .core.module_registry import ModuleRegistry
from .utils import sha256_file


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _source_pdf(root: Path, record: DocumentRecord) -> Path | None:
    for candidate in root.rglob(record.filename):
        if candidate.is_file() and "SKBUK" not in candidate.parts:
            return candidate
    return None


def _metadata(record: DocumentRecord, relative_pdf: str, modules: tuple[str, ...]) -> dict:
    return {
        "document_id": record.document_id,
        "title": record.title,
        "pdf_path": relative_pdf,
        "source_url": record.source_url,
        "landing_page_url": record.landing_page_url,
        "publisher": record.publisher,
        "document_type": record.document_type,
        "legislation_or_policy_reference": record.legislation_or_policy_reference,
        "publication_date": record.publication_date,
        "last_checked_at": record.last_checked_at,
        "downloaded_at": record.downloaded_at,
        "http_last_modified": record.http_last_modified,
        "etag": record.etag,
        "sha256": record.sha256,
        "status": record.status,
        "relevance_tags": record.relevance_tags,
        "supersedes": record.supersedes,
        "superseded_by": record.superseded_by,
        "mouuk_modules": list(modules),
        "processing_stage": "raw_pdf_reference",
        "chunked": False,
        "embedded": False,
        "summarised": False,
    }


def sync_records(root: Path, records: list[DocumentRecord], dry_run: bool = False) -> dict:
    """Materialise registered active PDFs into SKBUK and publish MOUUK manifests."""
    skbuk = root / "SKBUK"
    documents = skbuk / "documents"
    manifests = skbuk / "delivery" / "MOUUK"
    audit_log = skbuk / "audit" / "events.jsonl"

    if not dry_run:
        documents.mkdir(parents=True, exist_ok=True)
        manifests.mkdir(parents=True, exist_ok=True)
        audit_log.parent.mkdir(parents=True, exist_ok=True)

    module_entries: dict[str, list[dict]] = {
        definition.code: [] for definition in ModuleRegistry.load()
    }
    synced = 0
    missing = 0

    for record in records:
        # Historical/superseded versions remain in the collector archive and registry,
        # but only the active version is delivered to MOUUK.
        if record.status != "active":
            continue
        source = _source_pdf(root, record)
        if source is None:
            missing += 1
            continue

        modules = route_modules(record.category, record.relevance_tags, record.title)
        doc_dir = documents / record.document_id
        target_pdf = doc_dir / record.filename
        target_meta = doc_dir / "metadata.json"
        relative_pdf = str(target_pdf.relative_to(root)).replace("\\", "/")
        metadata = _metadata(record, relative_pdf, modules)

        if not dry_run:
            doc_dir.mkdir(parents=True, exist_ok=True)
            if not target_pdf.exists() or sha256_file(target_pdf) != record.sha256:
                shutil.copy2(source, target_pdf)
            target_meta.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            with audit_log.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"timestamp": _now(), "event": "document_synced", "document_id": record.document_id, "sha256": record.sha256, "source_url": record.source_url, "modules": list(modules)}, ensure_ascii=False) + "\n")

        for module in modules:
            module_entries.setdefault(module, []).append({
                "document_id": record.document_id,
                "title": record.title,
                "pdf_path": relative_pdf,
                "metadata_path": str(target_meta.relative_to(root)).replace("\\", "/"),
                "source_url": record.source_url,
                "landing_page_url": record.landing_page_url,
                "sha256": record.sha256,
                "status": record.status,
            })
        synced += 1

    if not dry_run:
        for module, entries in module_entries.items():
            path = manifests / f"{module}.json"
            payload = {
                "module": module,
                "role": "MOUUK expert knowledge module",
                "owner": "SKBUK",
                "source_of_truth": "SKBUK/documents",
                "documents": entries,
                "processing_stage": "raw_pdf_reference",
            }
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "documents_synced": synced,
        "documents_missing": missing,
        "modules_published": len(module_entries),
        "dry_run": dry_run,
    }
