from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, TypeVar

from pydantic import BaseModel

from .schema import Document


DOCUMENTS_CSV_HEADERS = [
    "document_id", "canonical_slug", "title", "publisher", "source_id", "document_family",
    "document_type", "jurisdiction", "applicability", "year", "language", "authoritative_url",
    "landing_url", "canonical_page_url", "first_seen_at", "first_seen_run_id", "latest_seen_at",
    "latest_seen_run_id", "latest_version_id", "latest_sha256", "latest_download_url",
    "latest_http_status", "latest_content_type", "latest_content_length", "latest_etag",
    "latest_last_modified", "latest_downloaded_at", "latest_file_name_original",
    "latest_file_path_current", "latest_file_path_versioned", "version_count", "status",
    "supersedes_document_id", "notes",
]

NULLABLE_FIELDS = {
    "jurisdiction", "applicability", "year", "canonical_page_url", "latest_version_id",
    "latest_sha256", "latest_download_url", "latest_http_status", "latest_content_type",
    "latest_content_length", "latest_etag", "latest_last_modified", "latest_downloaded_at",
    "latest_file_name_original", "latest_file_path_current", "latest_file_path_versioned",
    "supersedes_document_id", "notes",
}
INT_FIELDS = {"year", "latest_http_status", "latest_content_length", "version_count"}


def _json_row(model: BaseModel) -> dict[str, object]:
    return model.model_dump(mode="json")


def document_to_csv_row(document: Document) -> dict[str, object]:
    row = _json_row(document)
    return {header: "" if row.get(header) is None else row[header] for header in DOCUMENTS_CSV_HEADERS}


def write_documents_csv(output_path: Path, documents: Iterable[Document]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=DOCUMENTS_CSV_HEADERS, extrasaction="raise")
        writer.writeheader()
        for document in documents:
            writer.writerow(document_to_csv_row(document))


def write_documents_jsonl(output_path: Path, documents: Iterable[Document]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as jsonl_file:
        for document in documents:
            jsonl_file.write(json.dumps(_json_row(document), ensure_ascii=False) + "\n")


def csv_row_to_document(row: dict[str, str]) -> Document:
    payload: dict[str, object] = dict(row)
    for field_name in NULLABLE_FIELDS:
        if payload.get(field_name) == "":
            payload[field_name] = None
    for field_name in INT_FIELDS:
        if payload.get(field_name) not in (None, ""):
            payload[field_name] = int(str(payload[field_name]))
    return Document.model_validate(payload)


def read_documents_csv(input_path: Path) -> list[Document]:
    with input_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        return [csv_row_to_document(row) for row in csv.DictReader(csv_file)]


ModelT = TypeVar("ModelT", bound=BaseModel)


def write_jsonl(output_path: Path, models: Iterable[ModelT]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as jsonl_file:
        for model in models:
            jsonl_file.write(json.dumps(_json_row(model), ensure_ascii=False) + "\n")
