"""Publish SKBUK-owned document references to MOUUK module manifests."""

from __future__ import annotations

import json
from pathlib import Path


MODULE_CODES = tuple(f"MOUUK-{number:04d}" for number in range(1, 35))
_SOURCE_MODULES = {
    "guidance": ("MOUUK-0007", "MOUUK-0008", "MOUUK-0009", "MOUUK-0010"),
    "src_procurement_act_2023": ("MOUUK-0001",),
    "src_procurement_act_guidance": ("MOUUK-0007", "MOUUK-0008", "MOUUK-0009", "MOUUK-0010"),
    "src_procurement_policy_notes": ("MOUUK-0005",),
}
_GOVERNANCE_MODULES = ("MOUUK-0023", "MOUUK-0024", "MOUUK-0025", "MOUUK-0026")


def modules_for_source(source_id: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys((*_SOURCE_MODULES.get(source_id, ()), *_GOVERNANCE_MODULES)))


def publish_references(storage_root: Path, references: list[dict[str, str]]) -> int:
    """Write reference-only manifests; PDFs remain owned by SKBUK storage."""
    manifest_dir = storage_root / "delivery" / "MOUUK"
    entries = {code: [] for code in MODULE_CODES}
    for reference in references:
        for code in modules_for_source(reference["source_id"]):
            entries[code].append(reference)

    for code, documents in entries.items():
        path = manifest_dir / f"{code}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "module": code,
                    "owner": "SKBUK",
                    "source_of_truth": "SKBUK storage",
                    "processing_stage": "raw_pdf_reference",
                    "documents": documents,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return len(entries)
