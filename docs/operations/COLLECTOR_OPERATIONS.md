# Collector Operations

Status: **ACTIVE OPERATIONAL**  
Subsystem: SKBUK acquisition and custody

The original UK public-sector procurement PDF collector remains a foundational TODS subsystem. It discovers documents from configured official landing pages, applies source-access controls, validates PDFs, calculates hashes, classifies content, preserves prior versions, and records provenance.

It does not provide legal advice and must not bypass authentication, paywalls, CAPTCHAs, anti-bot systems, robots restrictions, or other access controls.

## Install

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Test first

```bash
python -m pytest -q
```

## Dry run

Dry-run validates and classifies temporary downloads but does not retain collected PDFs or add active document records. It may create runtime directories, logs, reports, and registry files.

```bash
python -m uk_kb_collector.main --dry-run
```

Review the run report and all source-access refusals before enabling production mode.

## Production run

```bash
python -m uk_kb_collector.main --production
```

Production collection should run only after configuration review, a successful dry run, storage/retention confirmation, and validation that no overlapping job is active.

## Configuration controls

- `config.yaml` controls collector behavior and runtime defaults.
- `sources.yml` lists source definitions where used by the active configuration path.
- `classification.yml` contains classification settings where used by the active classifier.
- `uk_kb_collector/modules.yaml` is the canonical MOUUK identity catalogue.

Configuration precedence must be verified in code before consolidating or deleting any of these files.

## Invariants

- Official and explicitly permitted sources only.
- Respect per-domain throttling and robots decisions.
- Bound retries, timeouts, and maximum file size.
- Validate content type and PDF magic bytes before storage.
- Never replace a changed document in place; preserve version history.
- Store source URL, publisher when known, check time, hash, version, and HTTP metadata.
- Send uncertain classification to review.
- Do not alter or summarise legal content during acquisition.
- Do not automatically delete archived source documents.

## Scheduling

Use the supplied scripts or an operating-system scheduler only after a successful manual production run. Prevent overlapping executions, capture stdout/stderr, set bounded retries, and monitor repeated source failures. Credentials must remain outside source control.
