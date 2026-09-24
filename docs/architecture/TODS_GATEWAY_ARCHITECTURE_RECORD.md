# TODS Gateway Architecture Record

Status: **CANONICAL**  
Decision scope: Product identity, trust boundary, principal components, and assurance behavior.

## Purpose

TODS Gateway is the regulatory and document-assurance gateway for public-service work. Every connected person, product, or AI agent should use the same controlled path when it relies on a rule, answers a regulated question, produces a material document, or prepares a report for public-service use.

TODS is both:

- the **first door**, controlling entry to governed regulatory and document intelligence; and
- the **final checkpoint**, reporting whether an output is supportable, limited, requires human review, or must be blocked.

## System boundary

```text
Caller
  |
  v
TODS Gateway
  |-- identity and authority
  |-- purpose and scope
  |-- policy selection
  |-- evidence requirements
  |-- assurance outcome
  |-- audit reference
  |
  +--> SKBUK: source acquisition, custody, validation, versioning, provenance
  |
  +--> MOUUK: stable specialist modules, rules, reasoning, citations, review flags
  |
  +--> Human review: accountable approval for consequential or uncertain outputs
```

## Component responsibilities

### TODS Gateway

- provides the common API and future SDK/CLI contract;
- validates caller, scope, request, and intended use;
- selects the appropriate assurance profile and specialist module;
- prevents unsupported confidence from becoming an official outcome;
- returns evidence, limitations, review requirements, and audit references.

### SKBUK

- discovers material only from configured and permitted sources;
- respects source-access and robots controls;
- validates document type and integrity;
- records URL, publisher, retrieval/check time, hash, version, and supersession;
- preserves provenance and separates collection from interpretation;
- performs initial calibration and routes evidence for specialist work.

The original UK public-sector procurement collector is retained as a foundational SKBUK subsystem, not discarded or renamed out of history.

### MOUUK

- consists of 34 stable specialist identities, `MOUUK-0001` through `MOUUK-0034`;
- receives governed evidence rather than crawling independently;
- applies module-specific taxonomy, rules, and reasoning;
- returns standard evidence-first responses with citations, confidence, and review flags;
- never converts missing evidence into a confident answer.

The canonical catalogue is `uk_kb_collector/modules.yaml`. Convenience registries must derive from or agree with that source.

## Trust model

A TODS response is trustworthy only when the material claim can be traced through this chain:

```text
claim
  -> evidence item
  -> immutable document hash and version
  -> source URL and publisher
  -> collection/check event
  -> applicable module and rule/policy version
  -> gateway release and audit event
```

Failure at any required link lowers the outcome or sends the request to review.

## Assurance outcomes

| Outcome | Meaning |
|---|---|
| `VERIFIED` | Required evidence and controls passed for the declared scope. |
| `VERIFIED_WITH_LIMITATIONS` | Core checks passed, with explicit bounded limitations. |
| `NEEDS_HUMAN_REVIEW` | A qualified person must decide before reliance or release. |
| `INSUFFICIENT_EVIDENCE` | The available evidence cannot support the requested conclusion. |
| `STALE_SOURCE_RISK` | Relevant material may be superseded or insufficiently current. |
| `OUT_OF_SCOPE` | The request is outside the selected module/profile or authority. |
| `BLOCKED` | Policy, security, authority, or integrity control prevents processing. |

The initial implementation must not emit production-grade `VERIFIED` solely from keyword matching.

## Current implementation

At this baseline:

- `main.py` provides `GET /` and `POST /api/v1/process-regulation`;
- SKBUK calibration is an initial deterministic keyword/length check;
- direct gateway processing exists for the Procurement Act module path;
- the collector architecture contains stronger evidence, provenance, registry, and plugin contracts;
- tests assert the complete stable catalogue and independent loading of all 34 specialist workers.

This distinction between **implemented**, **tested**, **planned**, and **production-approved** is mandatory in all project documents.

## Mandatory controls before production assurance

- authenticated caller and scoped authorization;
- request and document integrity validation;
- canonical source/version resolution;
- evidence-to-claim linkage;
- policy and module version capture;
- explicit limitation and uncertainty handling;
- durable audit event and correlation ID;
- human approval for defined risk classes;
- security, privacy, evaluation, rollback, and monitoring gates.

## Architectural decisions

1. Collection and specialist reasoning remain separated.
2. Stable MOUUK IDs are never silently reused.
3. Official claims require evidence lineage, not model confidence alone.
4. Unknown or ambiguous cases fail toward review, not certainty.
5. Historical artefacts are archived and labelled; history is not rewritten.
6. Documentation describes executable reality and labels roadmap work clearly.
7. All internal projects use the gateway contract rather than implementing conflicting assurance logic independently.
