# SKBUK — Knowledge Supply & Governance

SKBUK is the central document layer for UKKB.

## Responsibilities

- ingest approved source documents from the Collector;
- keep the original PDF as the source of truth;
- preserve source URL and landing-page URL;
- preserve publisher, jurisdiction, publication/update dates and version metadata;
- calculate and retain SHA-256 hashes;
- maintain supersession/version history;
- audit every ingest/update/delivery event;
- publish delivery manifests to MOUUK-0001 through MOUUK-0034;
- never chunk, embed or summarise during the raw-document collection phase.

## Tree

```text
SKBUK/
├── documents/
│   └── <document_id>/
│       ├── original.pdf
│       └── metadata.json
├── delivery/
│   └── MOUUK/
│       ├── MOUUK-0001.json
│       ├── MOUUK-0002.json
│       ├── ...
│       └── MOUUK-0034.json
├── audit/
│   └── events.jsonl
└── README.md
```

`SKBUK/documents` is the canonical storage location. MOUUK receives references/manifests and must not become the source-of-truth owner of the PDFs.

## Verified repository status - 30 August 2026

This checkout has 34 MOUUK delivery manifests, but no canonical PDF files and no registry records. The latest recorded collector report found 421 PDF links from 438 checked URLs, with 0 new and 0 updated files and 20 robots-policy refusals. This means the report is an ingestion check, not proof that the full corpus is currently present locally; refused sources remain unverified.
