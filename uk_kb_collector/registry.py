from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .models import DocumentRecord, REGISTRY_FIELDS


class Registry:
    def __init__(self, csv_path: Path, json_path: Path) -> None:
        self.csv_path = csv_path
        self.json_path = json_path
        self.records: dict[str, DocumentRecord] = {}
        self.by_url: dict[str, DocumentRecord] = {}
        self.by_hash: dict[str, DocumentRecord] = {}
        self.by_filename: dict[str, DocumentRecord] = {}

    def load(self) -> None:
        if self.json_path.exists():
            data = json.loads(self.json_path.read_text(encoding="utf-8"))
            rows = data if isinstance(data, list) else data.get("documents", [])
        elif self.csv_path.exists():
            with self.csv_path.open("r", newline="", encoding="utf-8-sig") as f:
                rows = list(csv.DictReader(f))
        else:
            rows = []
        for row in rows:
            row["file_size_bytes"] = int(row.get("file_size_bytes") or 0)
            tags = row.get("relevance_tags", [])
            if isinstance(tags, str):
                try:
                    row["relevance_tags"] = json.loads(tags) if tags.startswith("[") else [x for x in tags.split(";") if x]
                except json.JSONDecodeError:
                    row["relevance_tags"] = [x for x in tags.split(";") if x]
            rec = DocumentRecord(**{k: row.get(k, "") for k in DocumentRecord.__dataclass_fields__})
            self.records[rec.document_id] = rec
            self.by_url[rec.source_url] = rec
            self.by_hash[rec.sha256] = rec
            self.by_filename[rec.filename] = rec

    def all(self) -> Iterable[DocumentRecord]:
        return self.records.values()

    def put(self, record: DocumentRecord) -> None:
        old = self.records.get(record.document_id)
        if old:
            self.by_url.pop(old.source_url, None)
            self.by_hash.pop(old.sha256, None)
            self.by_filename.pop(old.filename, None)
        self.records[record.document_id] = record
        self.by_url[record.source_url] = record
        if record.sha256:
            self.by_hash[record.sha256] = record
        self.by_filename[record.filename] = record

    def find_by_url(self, url: str) -> DocumentRecord | None:
        return self.by_url.get(url)

    def find_by_hash(self, sha256: str) -> DocumentRecord | None:
        return self.by_hash.get(sha256)

    def find_by_filename(self, filename: str) -> DocumentRecord | None:
        return self.by_filename.get(filename)

    def save(self) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        rows = [r.to_dict() for r in self.records.values()]
        with self.csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=REGISTRY_FIELDS)
            writer.writeheader()
            for row in rows:
                row = dict(row)
                row["relevance_tags"] = ";".join(row["relevance_tags"])
                writer.writerow(row)
        self.json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
