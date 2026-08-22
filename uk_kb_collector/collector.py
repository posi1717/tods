from __future__ import annotations

import logging
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from .categorize import classify
from .config import CollectorConfig
from .discover import PdfCandidate, discover_pdfs
from .http import SafeHttpClient
from .models import DocumentRecord
from .pdf import pdf_metadata, validate_pdf
from .registry import Registry
from .utils import build_filename, document_id, next_version, sha256_file, version_document_id

LOG = logging.getLogger(__name__)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_dirs(root: Path) -> dict[str, Path]:
    dirs = {
        "root": root, "inbox": root / "00_Inbox", "legislation": root / "01_Legislation",
        "statutory": root / "02_Statutory_Guidance", "ppns": root / "03_Procurement_Policy_Notes",
        "policy": root / "04_NPPS_and_Government_Policy", "cabinet": root / "05_Cabinet_Office_Guidance",
        "frameworks": root / "06_Frameworks_Standards_Playbooks", "templates": root / "07_Templates_and_Model_Documents",
        "archive": root / "08_Archive", "logs": root / "09_Logs", "metadata": root / "10_Metadata",
        "temp": root / "00_Inbox" / ".tmp",
    }
    for p in dirs.values():
        p.mkdir(parents=True, exist_ok=True)
    for p in [dirs["legislation"] / "Procurement_Act_2023", dirs["legislation"] / "Procurement_Regulations_2024", dirs["legislation"] / "Legacy_Regulations", dirs["legislation"] / "Other_Relevant_Legislation", dirs["cabinet"] / "Plan", dirs["cabinet"] / "Define", dirs["cabinet"] / "Procure", dirs["cabinet"] / "Manage"]:
        p.mkdir(parents=True, exist_ok=True)
    return dirs


def category_dir(dirs: dict[str, Path], category: str) -> Path:
    mapping = {
        "00_Inbox": dirs["inbox"],
        "01_Legislation/Procurement_Act_2023": dirs["legislation"] / "Procurement_Act_2023",
        "01_Legislation/Procurement_Regulations_2024": dirs["legislation"] / "Procurement_Regulations_2024",
        "01_Legislation/Legacy_Regulations": dirs["legislation"] / "Legacy_Regulations",
        "01_Legislation/Other_Relevant_Legislation": dirs["legislation"] / "Other_Relevant_Legislation",
        "02_Statutory_Guidance": dirs["statutory"],
        "03_Procurement_Policy_Notes": dirs["ppns"],
        "04_NPPS_and_Government_Policy": dirs["policy"],
        "05_Cabinet_Office_Guidance/Plan": dirs["cabinet"] / "Plan",
        "05_Cabinet_Office_Guidance/Define": dirs["cabinet"] / "Define",
        "05_Cabinet_Office_Guidance/Procure": dirs["cabinet"] / "Procure",
        "05_Cabinet_Office_Guidance/Manage": dirs["cabinet"] / "Manage",
        "06_Frameworks_Standards_Playbooks": dirs["frameworks"],
        "07_Templates_and_Model_Documents": dirs["templates"],
    }
    return mapping.get(category, dirs["inbox"])


def _existing_filename_candidates(record: DocumentRecord | None, target_dir: Path) -> list[str]:
    names = [p.name for p in target_dir.glob("*.pdf")]
    if record:
        names.append(record.filename)
    return sorted(set(names))


def run_once(config: CollectorConfig, logger: logging.LoggerAdapter) -> dict:
    dirs = build_dirs(config.destination)
    reg = Registry(dirs["metadata"] / "document_registry.csv", dirs["metadata"] / "document_registry.json")
    reg.load()
    client = SafeHttpClient(config)
    started = time.monotonic()
    candidates, pages_checked, discovery_errors = discover_pdfs(config, client)

    summary = {
        "urls_checked": pages_checked, "pdfs_found": len(candidates), "new": 0, "updated": 0,
        "skipped": 0, "failed": [], "new_docs": [], "supersedes": [], "needs_review": [],
    }
    for err in discovery_errors:
        summary["failed"].append(err)

    for index, candidate in enumerate(candidates[:config.max_candidates_per_run], start=1):
        if time.monotonic() - started >= config.max_run_minutes * 60:
            logger.warning("Run time limit reached after %s candidates; remaining candidates will be handled next run", index - 1)
            break
        logger.info("Processing PDF %s/%s: %s", index, min(len(candidates), config.max_candidates_per_run), candidate.source_url)
        try:
            process_candidate(config, dirs, reg, client, candidate, summary, logger)
        except Exception as exc:
            msg = f"{candidate.source_url} :: {type(exc).__name__}: {exc}"
            summary["failed"].append(msg)
            logger.error(msg)
    reg.save()
    return summary


def process_candidate(config: CollectorConfig, dirs: dict[str, Path], reg: Registry, client: SafeHttpClient, candidate: PdfCandidate, summary: dict, logger: logging.LoggerAdapter) -> None:
    url = candidate.source_url
    if not client.robots_allowed(url):
        summary["failed"].append(f"robots.txt disallowed: {url}")
        return
    if not urlparse(url).scheme.startswith("http"):
        summary["failed"].append(f"unsupported URL scheme: {url}")
        return

    current = reg.find_by_url(url)
    conditional = {}
    if current:
        if current.etag:
            conditional["If-None-Match"] = current.etag
        if current.http_last_modified:
            conditional["If-Modified-Since"] = current.http_last_modified

    response = client.get(url, headers=conditional, stream=True)
    if response.status_code == 304 and current:
        current.last_checked_at = now_iso()
        reg.put(current)
        summary["skipped"] += 1
        return
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    declared_length = int(response.headers.get("Content-Length") or 0) or None
    if declared_length and declared_length > config.max_pdf_bytes:
        raise ValueError("Content-Length exceeds configured maximum")

    temp = dirs["temp"] / f"{document_id(url)}.download"
    temp.unlink(missing_ok=True)
    with temp.open("wb") as f:
        size = 0
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if not chunk:
                continue
            size += len(chunk)
            if size > config.max_pdf_bytes:
                raise ValueError("download exceeded configured maximum size")
            f.write(chunk)
    response.close()
    validate_pdf(temp, content_type, declared_length, config.max_pdf_bytes)
    digest = sha256_file(temp)

    duplicate = reg.find_by_hash(digest)
    if duplicate and (current is None or duplicate.document_id != current.document_id):
        temp.unlink(missing_ok=True)
        summary["skipped"] += 1
        logger.info("Skipping duplicate SHA-256 already registered as %s: %s", duplicate.document_id, url)
        return

    if current and current.sha256 == digest:
        current.last_checked_at = now_iso()
        current.http_last_modified = client.http_date_value(response.headers.get("Last-Modified", ""))
        current.etag = response.headers.get("ETag", "")
        reg.put(current)
        temp.unlink(missing_ok=True)
        summary["skipped"] += 1
        return

    meta = pdf_metadata(temp, config.max_pdf_probe_pages, config.max_relevance_chars)
    title = candidate.landing_title or meta.get("title") or Path(urlparse(url).path).stem or "Untitled document"
    classification = classify(url, title, meta, candidate.category_hint, config.keywords.get("tags", {}))
    publisher = classification.publisher if classification.publisher != "unknown-publisher" else candidate.publisher_hint or "unknown-publisher"
    publication_date = candidate.publication_date or ""
    last_modified = client.http_date_value(response.headers.get("Last-Modified", ""))
    version_files = _existing_filename_candidates(current, category_dir(dirs, classification.category))
    version = next_version(version_files) if current else 1
    filename = build_filename(publication_date, publisher, title, version)
    target_dir = category_dir(dirs, classification.category)
    target = target_dir / filename
    while target.exists():
        version += 1
        filename = build_filename(publication_date, publisher, title, version)
        target = target_dir / filename

    if config.dry_run:
        logger.info("DRY-RUN would store %s -> %s", url, target)
        temp.unlink(missing_ok=True)
        summary["new" if current is None else "updated"] += 1
        if current:
            summary["supersedes"].append({"new_title": title, "old_filename": current.filename, "url": url})
        else:
            summary["new_docs"].append({"title": title, "category": classification.category, "publisher": publisher, "url": url})
        if classification.needs_review:
            summary["needs_review"].append({"title": title, "url": url})
        return

    if current:
        old_path = locate_existing(config.destination, current.filename)
        if old_path and old_path.exists():
            archive_name = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}__{old_path.name}"
            archive_target = dirs["archive"] / archive_name
            shutil.move(str(old_path), str(archive_target))
            current.status = "superseded"
            reg.put(current)

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(temp), str(target))
    new_id = version_document_id(url, digest) if current else document_id(url)
    rec = DocumentRecord(
        document_id=new_id,
        title=title,
        filename=filename,
        category=classification.category,
        source_url=url,
        landing_page_url=candidate.landing_page_url,
        publisher=publisher,
        document_type=classification.document_type,
        legislation_or_policy_reference=classification.legislation_or_policy_reference or candidate.reference_hint,
        publication_date=publication_date,
        last_checked_at=now_iso(),
        downloaded_at=now_iso(),
        file_size_bytes=target.stat().st_size,
        sha256=digest,
        http_last_modified=last_modified,
        etag=response.headers.get("ETag", ""),
        status="active",
        relevance_tags=classification.tags,
        notes=classification.notes,
        supersedes=current.document_id if current else "",
        superseded_by="",
    )
    if current:
        current.superseded_by = rec.document_id
        reg.put(current)
    reg.put(rec)
    summary["updated" if current else "new"] += 1
    if current:
        summary["supersedes"].append({"new_title": title, "old_filename": current.filename, "url": url})
    else:
        summary["new_docs"].append({"title": title, "category": classification.category, "publisher": publisher, "url": url})
    if classification.needs_review:
        summary["needs_review"].append({"title": title, "url": url})


def locate_existing(root: Path, filename: str) -> Path | None:
    for p in root.rglob(filename):
        if p.is_file():
            return p
    return None
