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
- [x] Record the gap between the gateway baseline and the wider collector/plugin architecture.
- [x] Verify configuration precedence across `config.yaml`, `sources.yml`, `classification.yml`, package settings, and environment variables.
- [x] Reconcile the early `MOUUK/mouuk_registry.py` subset with the canonical YAML registry without deleting either path prematurely.

## Batch B — Service foundation

- [x] Replace the collector-only README identity with TODS Gateway identity while preserving collector operations.
- [x] Create the canonical TODS architecture record.
- [x] Create the canonical-document register.
- [x] Create an API deployment register based on executable routes.
- [x] Move detailed collector operation guidance into an operations document.
- [x] Document data governance, lifecycle, implemented schema families, and reconciliation gates.
- [x] Build a responsive enterprise assurance console against the real gateway API.
- [x] Add machine-readable service status and per-request correlation IDs.
- [x] Add a non-root container, Compose service, and health check.
- [x] Add an enterprise-console runbook and service-readiness assessment.
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
- [x] Add configuration-precedence and MOUUK compatibility tests.
- [x] Run the complete test suite in a clean checkout: 67 passed.
- [x] Run a live local smoke test for the UI, status API, assessment API, and correlation ID.
- [x] Check internal links across 194 Markdown files: no broken local links.
- [x] Add CI jobs for the complete test suite and container smoke test.
- [ ] Confirm the GitHub-hosted CI run and resolve any platform-specific failure.
- [ ] Run repository secret scanning when GitHub Advanced Security is enabled or through an approved alternative scanner.
- [x] Open a draft pull request.
- [ ] Review the final diff before marking the pull request ready.

## Deferred production controls

These items are not represented as complete in this service baseline:

- production authentication and scoped authorization;
- durable audit-event storage;
- signed evidence and assurance receipts;
- policy/rule-pack lifecycle management;
- complete gateway routing across all 34 MOUUK modules;
- durable human approval workflow;
- production SDK and CLI;
- hosted-service deployment and operational certification.

## Definition of done

The controlled service baseline is complete when the UI and API are executable, repository tests pass, runtime packaging exists, documentation agrees with behavior, no protected historical/source material is deleted, and a reviewable pull request records all changes. Public production readiness additionally requires the deferred controls and service-owner approval.
