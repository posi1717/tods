# TODS Gateway Master Change List

Status: **ACTIVE**  
Scope: `posi1717/tods`  
Working branch: `chore/tods-gateway-governance-baseline`

This list controls the transition from the original collector-focused repository presentation to the TODS regulatory and document-assurance gateway. It is intentionally incremental and reversible.

## Non-negotiable safeguards

- Preserve the working collector and its official-source safeguards.
- Preserve SKBUK source custody, provenance, hash, versioning, and calibration work.
- Preserve stable module IDs `MOUUK-0001` through `MOUUK-0034`.
- Preserve migration history, evidence records, tests, and Git history.
- Do not describe planned controls or endpoints as deployed.
- Do not issue production assurance from a keyword-only or unsupported decision path.
- Do not delete logs, corpus material, temporary downloads, or historical documents until dependency and retention checks are complete.

## Batch A — Baseline and truth

- [x] Create an isolated working branch from `main`.
- [x] Inventory repository root and existing documentation.
- [x] Verify the executable FastAPI routes in `main.py`.
- [x] Identify `uk_kb_collector/modules.yaml` as the canonical 34-module catalogue.
- [x] Confirm architecture/governance tests assert 34 stable and independently loadable modules.
- [x] Record the gap between the two-route gateway baseline and the wider collector/plugin architecture.
- [ ] Verify configuration precedence across `config.yaml`, `sources.yml`, `classification.yml`, package settings, and environment variables.
- [ ] Reconcile the early `MOUUK/mouuk_registry.py` subset with the canonical YAML registry without deleting either path prematurely.

## Batch B — Documentation foundation

- [x] Replace the collector-only README identity with TODS Gateway identity while preserving collector operations.
- [x] Create the canonical TODS architecture record.
- [x] Create the canonical-document register.
- [x] Create an API deployment register based on executable routes.
- [x] Move detailed collector operation guidance into an operations document.
- [ ] Review and align `SKBUK_ARCHITECTURE.md` with implemented package boundaries.
- [ ] Reconcile the Markdown and PDF MOUUK catalogue; Markdown remains the editable source.

## Batch C — Historical material

- [x] Create an archive policy and location.
- [ ] Classify `project_info__1.md`, `project_info__2.md`, and `project_info__3.md` after content review.
- [ ] Move only confirmed historical snapshots into `docs/archive/` in a dedicated commit.
- [ ] Add historical/non-canonical banners to archived documents.

## Batch D — Repository hygiene

- [x] Extend `.gitignore` for environments, caches, secrets, build output, collector temporary files, and runtime logs.
- [ ] Identify already tracked runtime artefacts; `.gitignore` alone does not untrack them.
- [ ] Produce a separate removal candidate list with dependency and retention evidence.
- [ ] Obtain explicit approval before deleting tracked logs, downloads, source material, or generated records.

## Batch E — Verification

- [x] Add documentation-governance and route-inventory tests.
- [ ] Run the complete test suite in CI.
- [ ] Resolve failures without weakening architecture, provenance, or evidence assertions.
- [ ] Check internal Markdown links.
- [ ] Scan changed content for secrets.
- [ ] Review the final diff and open a draft pull request.

## Deferred implementation

These items are not represented as complete in this baseline:

- production authentication and scoped authorization;
- durable audit-event storage;
- signed evidence and assurance receipts;
- policy/rule-pack lifecycle management;
- complete gateway routing across all 34 MOUUK modules;
- human approval workflow;
- production SDK and CLI;
- hosted-service deployment and operational certification.

## Definition of done

The baseline is done when README and canonical documents agree with executable code, existing tests remain green, new governance tests pass, no secret is introduced, no protected historical/source material is deleted, and a reviewable pull request records all changes.
