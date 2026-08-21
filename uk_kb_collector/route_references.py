from __future__ import annotations

import shutil
from pathlib import Path

from .module_routing import module_reference_dirs, route_modules


def route_registered_pdfs(root: Path, registry_rows: list[dict]) -> dict:
    """Copy already-collected PDFs into module reference folders.

    PDF bytes are copied unchanged. This stage does not extract, chunk,
    embed, summarize, or otherwise transform document content.
    """
    routed = 0
    missing = 0
    modules_seen: dict[str, int] = {}

    for row in registry_rows:
        if row.get("status") != "active":
            continue
        filename = row.get("filename", "")
        if not filename:
            continue
        source = next(root.rglob(filename), None)
        if source is None or not source.is_file():
            missing += 1
            continue

        tags = [x for x in row.get("relevance_tags", "").replace(";", ",").split(",") if x]
        modules = route_modules(row.get("category", ""), tags, row.get("title", ""))
        refs = module_reference_dirs(root, modules)
        for code, ref_dir in refs.items():
            target = ref_dir / source.name
            if not target.exists() or target.stat().st_size != source.stat().st_size:
                shutil.copy2(source, target)
                routed += 1
            modules_seen[code] = modules_seen.get(code, 0) + 1

    return {"routed_copies": routed, "missing": missing, "modules": modules_seen}
