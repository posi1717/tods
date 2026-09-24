# Data Governance and Lifecycle

**Status:** Canonical baseline  
**Version:** 0.1  
**Updated:** 24 September 2026

## Purpose

This document defines how TODS Gateway must govern regulatory sources, documents, evidence, specialist assessments, review decisions, and assurance records. It distinguishes the database structures that exist today from the complete lifecycle required for production assurance.

## Governing principles

1. Official source material is evidence input, not an automatically correct final answer.
2. A logical document and each downloaded binary version have separate identities.
3. A version is immutable once its integrity hash and custody record are accepted.
4. Superseded material is retained and marked; it is not silently overwritten.
5. A material claim must link to evidence from a specific document version.
6. A decision must disclose source freshness, limitations, and review status.
7. Tenant, bidder, tender, and official-source material must remain access-controlled and auditable.
8. Deletion requires an approved retention rule and evidence that legal, audit, operational, and dependency obligations are satisfied.

## Implemented schema families

The repository currently contains two related SQL schema families. They are not yet a single reconciled production migration chain.

### Collector registry migrations

`supabase/migrations/20260826020122_create_uk_kb_registry_schema.sql` defines:

- `sources` for approved landing pages and robots status;
- `runs` for collector execution outcomes;
- `documents` for logical document identity and latest-version reporting fields;
- `document_versions` for immutable binary revisions and SHA-256 lineage;
- `rejections` for controlled collection failures;
- enums, constraints, indexes, RLS enablement, revoked browser roles, and service-role access.

This schema uses text identifiers and storage paths under `data/documents/`.

### SKBUK service SQL

`SKBUK/sql/001_skbuk_schema.sql` defines a separate `tod_*` namespace including:

- taxonomy, organisations, and tenders;
- source documents and immutable versions;
- source excerpts with extractor identity, page ranges, and text hashes;
- inspection runs and the versions locked to each inspection;
- compliance checks and their evidence excerpt IDs;
- ingestion runs/events and document-to-module routing.

`SKBUK/sql/002_skbuk_storage_rls.sql` creates private storage buckets and enables RLS while deliberately creating no anonymous/browser storage policy.

`SKBUK/sql/003_skbuk_seed_taxonomy.sql` seeds bidder categories and only a subset of official MOUUK taxonomy codes. It is not a complete 34-module catalogue; `uk_kb_collector/modules.yaml` remains authoritative for module identity.

## Schema reconciliation rule

The two schema families overlap in source-document and version concepts but differ in naming, identifier types, lineage details, and operational scope. They must not both be described as one deployed schema until an explicit migration and compatibility design exists.

For the current repository:

- versioned files under `supabase/migrations/` are the authoritative migration history for a Supabase deployment;
- `SKBUK/sql/` is an active package-level schema design and must be promoted through new forward-only Supabase migrations before being treated as deployed;
- existing migration files must not be rewritten after application to a shared environment;
- reconciliation must use a new migration, data mapping, rollback plan, and integration tests.

## Lifecycle

```text
source registration
  -> access/robots decision
  -> discovery and collection run
  -> file validation and SHA-256
  -> logical document match/create
  -> immutable document version
  -> provenance and freshness metadata
  -> excerpt/evidence extraction
  -> route to stable MOUUK module(s)
  -> claim or compliance check
  -> limitations/conflict evaluation
  -> human review when required
  -> assurance decision and audit receipt
  -> retention, supersession, or approved disposal
```

## Record classes

| Record | Identity | Mutability rule | Current implementation |
|---|---|---|---|
| Source | Stable source ID | Metadata may change with audit history | Implemented in collector migration |
| Collection run | Unique run ID | Append/finish status; never reuse | Implemented in collector migration |
| Logical document | Stable document ID/slug | Current-state fields may advance | Implemented in both schema families |
| Document version | Unique version ID plus SHA-256 | Immutable after acceptance | Implemented in both schema families |
| Rejection | Unique rejection ID | Append-only operational evidence | Implemented in collector migration |
| Source excerpt | Unique excerpt ID plus text hash | Immutable for a document version/extractor version | Implemented in SKBUK SQL design |
| Inspection snapshot | Unique inspection run | Locks source versions before decision | Implemented in SKBUK SQL design |
| Module route | Document/excerpt to stable module code | Versioned/rerunnable policy required | Implemented in SKBUK SQL design |
| Claim | Unique claim ID linked to evidence | Required in application contracts; database persistence not reconciled | Partial Python contract only |
| Assurance decision | Unique decision linked to policy/review | Required; not yet a reconciled database record | Not production-implemented |
| Audit receipt | Immutable correlation and lineage record | Append-only and tamper-evident target | Not production-implemented |
| Agent action | Actor, scope, tool, input/output and decision | Append-only according to retention policy | Not production-implemented |

## Access control

Existing SQL takes a deny-by-default direction: relevant tables have RLS enabled, browser roles are revoked, storage buckets are private, and no anonymous storage policy is created. Production release still requires verification of service-role/object privileges, per-tenant policy, least-privilege service identities, key rotation, audit access, and recovery behavior in the actual environment.

Application code must not use the service role in a browser, client bundle, document, log, or repository file. Secrets belong in the deployment secret manager or approved vault.

## Freshness and supersession

A document can be authentic and still be unsuitable because it is obsolete or superseded. TODS must retain:

- the authoritative and landing URLs;
- first/latest seen timestamps;
- HTTP metadata where available;
- binary hash and version relationship;
- current/superseded/missing/rejected status;
- the source check used for the assurance decision.

A failed or blocked freshness check must produce `STALE_SOURCE_RISK`, `INSUFFICIENT_EVIDENCE`, or `NEEDS_HUMAN_REVIEW` according to the assurance profile. It must not silently reuse an old version as current.

## Evidence and claims

Evidence must point to a specific immutable version and, when extracted, preserve page/heading location, extractor identity/version, text hash, and extraction confidence. Claims must reference evidence IDs; unsupported claims cannot receive `VERIFIED`.

Conflicting evidence is retained and surfaced. TODS does not delete or hide a conflict to produce a cleaner answer.

## Retention and deletion

No universal retention period is asserted in this baseline. A production policy must classify at least:

- official source binaries and superseded versions;
- ingestion and rejection logs;
- tender and bidder documents;
- excerpts and derived evidence;
- inspection snapshots and compliance checks;
- assurance receipts and agent actions;
- temporary downloads and failed partial files.

Temporary files may be disposed of after job-state and forensic requirements are satisfied. Source versions, decision evidence, and audit records require an explicit policy owner, retention basis, legal review where applicable, and a recorded disposal event.

## Scheduling risk

Historical Supabase migrations schedule an hourly dispatch to `Donny1717/UKKB`, while the current GitHub workflow also has its own two-hour schedule and the active repository is `posi1717/tods`. Migration history is preserved, but the effective database cron job must be inspected before production use. A future forward-only migration should either point to the approved repository/workflow or remove the duplicate scheduler; it must retrieve credentials from the vault and never embed a token.

## Production gates

Before database-backed TODS assurance is described as production-ready:

1. choose and migrate to one reconciled source/document/version model;
2. define tenant and organisation ownership on all sensitive records;
3. implement evidence, claim, assurance-decision, review, audit-receipt, and agent-action persistence;
4. validate RLS and storage behavior with positive and negative integration tests;
5. define backup, restore, retention, disposal, and incident procedures;
6. reconcile GitHub and database scheduling to one approved operating model;
7. prove end-to-end lineage from request to immutable source version and final decision.
