# Service Readiness

**Assessment date:** 24 September 2026  
**Target:** TODS Gateway enterprise console service baseline

## Readiness decision

The branch is **ready for a controlled internal demonstration or supervised pilot deployment**. It is not approved for unsupervised public production assurance.

## Completed today

- Enterprise assurance console is served from the FastAPI root route.
- Responsive desktop, tablet, and mobile layouts are included without a separate frontend build dependency.
- Live status, regulatory submission, actual calibration/routing output, limitations, correlation ID, JSON copy, and decision-record download are implemented.
- The API and UI consistently require human review and do not emit production-grade `VERIFIED` outcomes.
- A non-root Python 3.12 Docker image and Docker Compose service are defined.
- Container and API health checks use `/api/v1/status`.
- CI installs declared root and SKBUK test dependencies, runs the full suite, builds the image, launches it, and smoke-tests the UI and status endpoint.
- A clean-checkout verification completed with 67 passing tests.
- A live local smoke test confirmed the console, status endpoint, assessment endpoint, and generated correlation ID.
- Internal links across 194 Markdown files were checked with no broken local links.

## Pilot launch checklist

- [x] Executable enterprise UI
- [x] Responsive and keyboard-accessible baseline
- [x] Honest service/capability status
- [x] Input validation and bounded request size
- [x] Human-review warning in API and UI
- [x] Correlation ID per assessment
- [x] Docker and Compose runtime definition
- [x] Automated unit/integration test workflow
- [x] Container smoke-test workflow
- [x] Operator runbook
- [ ] Select hosting environment and approved domain
- [ ] Configure TLS and edge request/rate limits
- [ ] Configure monitoring, alerts, backup, and rollback ownership
- [ ] Obtain service-owner acceptance for a supervised pilot

## Public production blockers

- Authentication and scoped authorization are not implemented.
- Correlation IDs are returned but durable tamper-evident audit storage is not implemented.
- Authoritative source identity, document version, freshness, and evidence linkage are not enforced by the current gateway route.
- Only MOUUK-0001 has direct specialist processing in this route; the other catalogue identities are not equivalent to deployed specialist execution.
- Human approval is communicated but there is no durable workflow or signer record.
- External penetration, privacy, accessibility, dependency-vulnerability, and operational recovery reviews remain outstanding.
- Database cron migrations target a historical repository and overlap the GitHub Actions schedule; the effective scheduler must be reconciled before enabling automated production collection.

## Approved claim

Use this wording for the current release:

> TODS Gateway provides a containerized enterprise assurance console for supervised evaluation of UK public-sector regulatory material. It exposes actual SKBUK calibration and current MOUUK routing behavior, returns traceable correlation IDs, and requires accountable human review.

Do not call the baseline a certified legal decision engine, fully autonomous assurance service, or production-ready public platform.
