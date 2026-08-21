# SKBUK / MOUUK Knowledge Architecture

## Ownership

- **SKBUK** is the knowledge supply and governance layer.
- **MOUUK-0001 ... MOUUK-0026** are specialist expert modules. They consume knowledge references; they do not own the source PDFs and do not crawl external sources.

## Lifecycle

```text
Official source
    |
    v
Collector
    |  validate PDF + SHA-256 + provenance
    v
SKBUK
    |  store + audit + version + update
    |
    +--> MOUUK delivery manifests (references only)
    |
    v
[future]
Extract -> Normalize -> Chunk -> Embed -> Retrieval
```

## SKBUK runtime layout

```text
SKBUK/
├── documents/
│   └── <document_id>/
│       ├── <original-pdf>.pdf
│       └── metadata.json
├── delivery/
│   └── MOUUK/
│       ├── MOUUK-0001.json
│       ├── ...
│       └── MOUUK-0026.json
└── audit/
    └── events.jsonl
```

`metadata.json` preserves the PDF's source URL, landing page, publisher, dates, version lineage, ETag/Last-Modified values, SHA-256 and the MOUUK modules to which SKBUK can deliver the document.

## Important boundary

The current stage is **raw PDF reference ingestion only**. It must not chunk, embed or summarise documents. Those stages start only after the SKBUK raw-document collection has been validated.

## Update behaviour

The collector checks the source URL and hash. Unchanged PDFs are skipped. Changed PDFs receive a new version and the previous copy remains in the archive/registry. SKBUK then refreshes its central copy and MOUUK delivery manifests and records a `document_synced` audit event.
