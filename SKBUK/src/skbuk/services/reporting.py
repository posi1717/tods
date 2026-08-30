from pathlib import Path
from typing import Mapping


def write_markdown(path: Path, run_id: str, sections: Mapping[str, list[str]]) -> Path:
    lines = [f"# SKBUK ingestion report: {run_id}", ""]
    for title, entries in sections.items():
        lines.extend([f"## {title}", ""])
        lines.extend([f"- {entry}" for entry in entries] or ["- None"])
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
