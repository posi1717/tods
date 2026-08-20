from __future__ import annotations

from datetime import datetime
from pathlib import Path


def write_report(log_dir: Path, summary: dict, dry_run: bool) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    path = log_dir / f"report_{stamp}.md"
    lines = [
        f"# UK Public Sector Procurement Collector Report — {stamp}",
        "",
        f"Mode: **{'DRY-RUN' if dry_run else 'PRODUCTION'}**",
        "",
        "## Summary",
        f"- URLs/pages checked: {summary['urls_checked']}",
        f"- PDFs found: {summary['pdfs_found']}",
        f"- New files: {summary['new']}",
        f"- Updated files: {summary['updated']}",
        f"- Skipped as unchanged/duplicate: {summary['skipped']}",
        f"- Failed: {len(summary['failed'])}",
        f"- Human review items: {len(summary['needs_review'])}",
        "",
        "## New documents",
    ]
    if summary["new_docs"]:
        for d in summary["new_docs"]:
            lines.append(f"- **{d['title']}** — `{d['category']}` — {d['publisher']} — {d['url']}")
    else:
        lines.append("- None")

    lines += ["", "## Documents likely superseding older versions"]
    if summary["supersedes"]:
        for d in summary["supersedes"]:
            lines.append(f"- **{d['new_title']}** likely supersedes `{d['old_filename']}` — {d['url']}")
    else:
        lines.append("- None")

    lines += ["", "## Failures"]
    if summary["failed"]:
        for e in summary["failed"]:
            lines.append(f"- {e}")
    else:
        lines.append("- None")

    lines += ["", "## Human review"]
    if summary["needs_review"]:
        for d in summary["needs_review"]:
            lines.append(f"- **{d['title']}** — {d['url']}")
    else:
        lines.append("- None")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
