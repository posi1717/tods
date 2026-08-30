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
│       └── MOUUK-0026.json
├── audit/
│   └── events.jsonl
└── README.md
```

`SKBUK/documents` is the canonical storage location. MOUUK receives references/manifests and must not become the source-of-truth owner of the PDFs.
