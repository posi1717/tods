from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse

from bs4 import BeautifulSoup

from .config import CollectorConfig
from .http import SafeHttpClient
from .utils import allowed_host

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class PdfCandidate:
    source_url: str
    landing_page_url: str
    landing_title: str
    publisher_hint: str
    category_hint: str
    reference_hint: str
    publication_date: str
    context_text: str


def _date_from_text(text: str) -> str:
    patterns = [
        r"\bPublished\s*[:\-]?\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
        r"\bPublished\s*[:\-]?\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            try:
                return datetime.strptime(m.group(1), "%d %B %Y").date().isoformat()
            except ValueError:
                try:
                    return datetime.strptime(m.group(1), "%d %b %Y").date().isoformat()
                except ValueError:
                    pass
    return ""


def _is_followable(url: str, seed_host: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname != seed_host:
        return False
    path = parsed.path.lower()
    return any(token in path for token in ("/government/publications/", "/government/guidance/", "/government/collections/", "/ukpga/", "/uksi/"))


def _relevant_candidate(text: str, href: str, source: dict, config: CollectorConfig) -> bool:
    low = (text + " " + href + " " + str(source.get("name", ""))).lower()
    if any(x.lower() in low for x in config.keywords.get("exclude", [])):
        return False
    if source.get("category_hint") in {"legislation", "procurement_regulations_2024", "legacy_regulations", "other_legislation", "procurement_policy_notes", "statutory_guidance", "government_policy"}:
        return True
    return any(x.lower() in low for x in config.keywords.get("include", []))


def discover_pdfs(config: CollectorConfig, client: SafeHttpClient) -> tuple[list[PdfCandidate], int, list[str]]:
    candidates: dict[str, PdfCandidate] = {}
    errors: list[str] = []
    pages_checked = 0
    for source in config.sources:
        seed = source["url"]
        if not allowed_host(seed, config.allowed_domains):
            errors.append(f"blocked source host: {seed}")
            continue
        if config.respect_terms_of_use and not allowed_host(seed, config.terms_approved_hosts):
            errors.append(f"terms-of-use host not approved in config: {seed}")
            continue
        if not client.robots_allowed(seed):
            errors.append(f"robots.txt disallowed: {seed}")
            continue
        seed_host = (urlparse(seed).hostname or "").lower()
        queue = deque([seed])
        visited: set[str] = set()
        while queue and len(visited) < config.max_discovery_pages_per_source:
            page = queue.popleft()
            if page in visited:
                continue
            visited.add(page)
            if not client.robots_allowed(page):
                errors.append(f"robots.txt disallowed: {page}")
                continue
            try:
                r = client.get(page)
                pages_checked += 1
                r.raise_for_status()
            except Exception as exc:
                errors.append(f"source fetch failed: {page} :: {exc}")
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.get_text(" ", strip=True) if soup.title else source.get("name", "")
            page_text = soup.get_text(" ", strip=True)[:40_000]
            publication_date = _date_from_text(page_text)
            for a in soup.find_all("a", href=True):
                href = urljoin(r.url, a["href"])
                href, _ = urldefrag(href)
                if not allowed_host(href, config.allowed_domains):
                    continue
                anchor_text = a.get_text(" ", strip=True)
                if href.lower().split("?")[0].endswith(".pdf") or ".pdf" in href.lower():
                    if not _relevant_candidate(anchor_text + " " + title, href, source, config):
                        continue
                    candidates[href] = PdfCandidate(
                        source_url=href,
                        landing_page_url=r.url,
                        landing_title=anchor_text or title,
                        publisher_hint=source.get("publisher_hint", ""),
                        category_hint=source.get("category_hint", ""),
                        reference_hint=source.get("reference_hint", ""),
                        publication_date=publication_date,
                        context_text=page_text,
                    )
                elif _is_followable(href, seed_host) and len(visited) + len(queue) < config.max_discovery_pages_per_source:
                    if href not in visited:
                        queue.append(href)
    return list(candidates.values()), pages_checked, errors
