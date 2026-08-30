# Registry schema

The canonical registry is split into logical documents and immutable binary versions.

- `documents.csv`: one row per logical document, with the latest version denormalised for reporting.
- `documents.jsonl`: one JSON object per logical document, suitable for ingestion jobs.
- `document_versions.jsonl`: one object per downloaded binary revision.
- `rejections.jsonl`: one object per rejected candidate and reason.
- `runs.jsonl`: one object per collector execution.
- `sources.yml`: allowlisted landing pages and source metadata.
- `classification.yml`: deterministic classification rules and controlled vocabularies.

The Pydantic models in `uk_kb_collector/schema.py` are the source of truth. Use
`uk_kb_collector/schema_io.py` for CSV and JSONL serialization. CSV is written as
UTF-8 with BOM (`utf-8-sig`) for reliable Windows/Excel display, and all paths are
relative POSIX paths rooted at `data/documents/`.

## Lifecycle rules

- `document_id` identifies the logical document and does not change when a PDF is replaced.
- `version_id` identifies one immutable binary revision.
- `latest_sha256` is the integrity key for the current binary; never use a placeholder hash.
- A changed hash creates a new `DocumentVersion`; the previous version remains immutable.
- `status` must be one of `active`, `superseded`, `missing`, or `rejected`.
- Rejection reasons are controlled by `RejectionReason`; free text belongs only in `detail`.
- Date-times must include a timezone and are normalised to UTC by the models.
- Official URLs are constrained to the approved government host policy.

## Example import

```python
from pathlib import Path
from uk_kb_collector.schema_io import read_documents_csv

documents = read_documents_csv(Path("data/documents.csv"))
```

The existing legacy registry remains available for backward compatibility. New
canonical records should use the schema layer before being sent to downstream
SKBUK or retrieval pipelines.
