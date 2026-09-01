"""Collect approved official PDFs into the immutable SKBUK document store."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx
import yaml

from skbuk.services.allowlist import approve
from skbuk.services.discovery import discover_links
from skbuk.services.downloader import download_pdf
from skbuk.services.delivery import publish_references
from skbuk.services.provenance import ProvenanceWriter
from skbuk.services.reporting import write_markdown
from skbuk.services.robots import check
from skbuk.services.storage import official_path, write_immutable
from skbuk.utils.filenames import safe_segment


@dataclass(frozen=True)
class CollectionResult:
    run_id: str
    sources_checked: int
    discovered: int
    stored: int
    would_store: int
    unchanged: int
    rejected: int
    errors: int
    modules_published: int
    report_path: Path

    def as_dict(self) -> dict[str, str | int]:
        return {
            "run_id": self.run_id,
            "sources_checked": self.sources_checked,
            "discovered": self.discovered,
            "stored": self.stored,
            "would_store": self.would_store,
            "unchanged": self.unchanged,
            "rejected": self.rejected,
            "errors": self.errors,
            "modules_published": self.modules_published,
            "report_path": str(self.report_path),
        }


def _load_sources(config_path: Path) -> list[dict]:
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("config sources must be a list")
    return [source for source in sources if source.get("enabled", True)]


def _pdf_links(client: httpx.Client, landing_url: str) -> list[str]:
    return [url for url in discover_links(client, landing_url) if urlparse(url).path.lower().endswith(".pdf")]


def collect(
    config_path: Path,
    storage_root: Path,
    user_agent: str,
    max_download_bytes: int,
    timeout_seconds: float,
    dry_run: bool = False,
    client: httpx.Client | None = None,
    provenance: ProvenanceWriter | None = None,
) -> CollectionResult:
    """Run discovery, policy checks, validation and immutable storage for enabled sources."""
    run_id = datetime.now(UTC).strftime("run-%Y%m%dT%H%M%SZ")
    report_path = storage_root / "reports" / f"{run_id}.md"
    sources_checked = discovered = stored = would_store = unchanged = rejected = errors = 0
    sections: dict[str, list[str]] = {"Sources checked": [], "Robots refusals": [], "Errors": []}
    references: list[dict[str, str]] = []
    owned_client = client is None
    client = client or httpx.Client(timeout=timeout_seconds, headers={"User-Agent": user_agent})

    try:
        if provenance and not dry_run:
            provenance.start()
        for source in _load_sources(config_path):
            source_id = str(source["source_id"])
            landing_url = str(source["landing_url"])
            sources_checked += 1
            sections["Sources checked"].append(source_id)
            if not approve(landing_url):
                rejected += 1
                sections["Errors"].append(f"{source_id}: host_not_allowlisted")
                continue
            landing_robots = check(client, landing_url, user_agent)
            if not landing_robots.allowed:
                rejected += 1
                sections["Robots refusals"].append(f"{source_id}: {landing_robots.status}")
                continue
            try:
                links = _pdf_links(client, landing_url)
            except (httpx.HTTPError, ValueError) as exc:
                errors += 1
                sections["Errors"].append(f"{source_id}: discovery failed: {exc}")
                continue

            for url in links:
                discovered += 1
                if not approve(url, landing_url):
                    rejected += 1
                    continue
                robots = check(client, url, user_agent)
                if not robots.allowed:
                    rejected += 1
                    sections["Robots refusals"].append(f"{url}: {robots.status}")
                    continue
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temporary = Path(temp_dir) / "download.pdf"
                        _, _, sha256 = download_pdf(client, url, temporary, max_download_bytes)
                        filename = f"{safe_segment(source_id)}__{sha256[:16]}.pdf"
                        relative_path = official_path(f"01_OFFICIAL_SOURCES/{safe_segment(source_id)}/{filename}")
                        target = storage_root / relative_path
                        newly_stored = False
                        if target.exists():
                            unchanged += 1
                        elif not dry_run:
                            write_immutable(storage_root, relative_path, temporary.read_bytes())
                            stored += 1
                            newly_stored = True
                        else:
                            would_store += 1
                        references.append({
                            "source_id": source_id,
                            "source_url": url,
                            "sha256": sha256,
                            "storage_path": relative_path,
                        })
                        if provenance and newly_stored:
                            provenance.accepted_document(source_id, url, sha256, relative_path)
                except (httpx.HTTPError, OSError, ValueError) as exc:
                    errors += 1
                    sections["Errors"].append(f"{url}: {exc}")
    finally:
        if owned_client:
            client.close()

    sections["Summary"] = [
        f"Discovered PDFs: {discovered}",
        f"Stored PDFs: {stored}",
        f"Would store PDFs: {would_store}",
        f"Unchanged PDFs: {unchanged}",
        f"Rejected URLs: {rejected}",
        f"Errors: {errors}",
        f"Dry run: {dry_run}",
    ]
    write_markdown(report_path, run_id, sections)
    modules_published = 0 if dry_run else publish_references(storage_root, references)
    if provenance and not dry_run:
        provenance.finish("completed" if errors == 0 else "partial", {
            "discovered": discovered,
            "stored": stored,
            "unchanged": unchanged,
            "rejected": rejected,
            "errors": errors,
        })
    return CollectionResult(run_id, sources_checked, discovered, stored, would_store, unchanged, rejected, errors, modules_published, report_path)
