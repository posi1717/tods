from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class CollectorConfig:
    destination: Path
    interval_hours: int
    dry_run: bool
    max_pdf_bytes: int
    connect_timeout: float
    read_timeout: float
    max_retries: int
    backoff_factor: float
    min_delay_per_domain: float
    user_agent: str
    verify_tls: bool
    max_pdf_probe_pages: int
    max_relevance_chars: int
    max_discovery_pages_per_source: int
    max_candidates_per_run: int
    max_run_minutes: int
    allowed_domains: tuple[str, ...]
    terms_approved_hosts: tuple[str, ...]
    respect_terms_of_use: bool
    sources: tuple[dict[str, Any], ...]
    keywords: dict[str, Any]
    legal_notice: str


def expand(path: str) -> Path:
    return Path(path).expanduser().resolve()


def load_config(path: Path) -> CollectorConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    c = raw["collector"]
    compliance = raw.get("compliance", {})
    return CollectorConfig(
        destination=expand(c["destination"]),
        interval_hours=int(c.get("interval_hours", 2)),
        dry_run=bool(c.get("dry_run", True)),
        max_pdf_bytes=int(c.get("max_pdf_bytes", 150_000_000)),
        connect_timeout=float(c.get("connect_timeout_seconds", 15)),
        read_timeout=float(c.get("read_timeout_seconds", 30)),
        max_retries=int(c.get("max_retries", 2)),
        backoff_factor=float(c.get("backoff_factor_seconds", 1.0)),
        min_delay_per_domain=float(c.get("min_delay_per_domain_seconds", 0.5)),
        user_agent=str(c["user_agent"]),
        verify_tls=bool(c.get("verify_tls", True)),
        max_pdf_probe_pages=int(c.get("max_pdf_probe_pages", 4)),
        max_relevance_chars=int(c.get("max_relevance_chars", 20_000)),
        max_discovery_pages_per_source=int(c.get("max_discovery_pages_per_source", 12)),
        max_candidates_per_run=int(c.get("max_candidates_per_run", 30)),
        max_run_minutes=int(c.get("max_run_minutes", 18)),
        allowed_domains=tuple(raw.get("allowed_domains", [])),
        terms_approved_hosts=tuple(compliance.get("terms_approved_hosts", [])),
        respect_terms_of_use=bool(compliance.get("respect_terms_of_use", True)),
        sources=tuple(raw.get("sources", [])),
        keywords=raw.get("keywords", {}),
        legal_notice=str(raw.get("notes", {}).get("legal_notice", "")),
    )
