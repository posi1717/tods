# SKBUK / MOUUK Knowledge Architecture

## Ownership

- **SKBUK** is the knowledge supply and governance layer.
- **MOUUK-0001 ... MOUUK-0034** are specialist expert modules. They consume knowledge references; they do not own the source PDFs and do not crawl external sources.

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
│       └── MOUUK-0034.json
└── audit/
    └── events.jsonl
```

`metadata.json` preserves the PDF's source URL, landing page, publisher, dates, version lineage, ETag/Last-Modified values, SHA-256 and the MOUUK modules to which SKBUK can deliver the document.

## Verified repository status - 30 August 2026

The repository contains the 34-module configuration and delivery-manifest structure, but this checkout contains no PDF files and the document registry has no records. The latest recorded collector run checked 438 URLs, found 421 PDF links, recorded 0 new and 0 updated files, and recorded 20 robots-policy refusals. Accordingly, document currency is not fully verifiable from the current checkout: successful URL checks support the unchanged result, while refused URLs remain unverified.

## Important boundary

The current stage is **raw PDF reference ingestion only**. It must not chunk, embed or summarise documents. Those stages start only after the SKBUK raw-document collection has been validated.

## Update behaviour

The collector checks the source URL and hash. Unchanged PDFs are skipped. Changed PDFs receive a new version and the previous copy remains in the archive/registry. SKBUK then refreshes its central copy and MOUUK delivery manifests and records a `document_synced` audit event.
