# API Deployment Register

Status: **CANONICAL OPERATIONAL**  
Source of executable truth: `main.py` on the corresponding release commit

This register separates routes that exist from capabilities that are planned. A route is not production assurance merely because it is executable.

## Current routes

| Method | Path | Implementation | Lifecycle | Assurance status |
|---|---|---|---|---|
| `GET` | `/` | `main.read_root` | Baseline | Informational only |
| `POST` | `/api/v1/process-regulation` | `main.process_regulation` | Baseline | Experimental; human review required |

Framework-generated OpenAPI and documentation routes are not counted as TODS business APIs.

## Current processing path

```text
RegulatoryInput
  -> SKBUKCalibrator.calibrate
  -> reject when baseline threshold fails
  -> direct MOUUK-0001 processing when Procurement Act routing matches
  -> pending-implementation response for other target routes
```

Current calibration uses document length and a small keyword set. It does not yet verify authoritative source identity, document hash/version, freshness, evidence linkage, authorization, or a durable audit record. Therefore, the endpoint must not claim a production-grade verified outcome.

## Deployment states

- `BASELINE`: executable development route; no public assurance promise.
- `INTERNAL_PILOT`: authenticated internal use with monitored evaluation.
- `LIMITED_PRODUCTION`: bounded scope, explicit users, implemented audit and rollback.
- `PRODUCTION`: approved controls, evaluation, operations, security, and ownership.
- `DEFERRED`: intentionally not active until prerequisites pass.
- `RETIRED`: unavailable; migration and historical reference retained.

## Planned contract groups

The following groups are architectural roadmap items, not deployed endpoints:

| Group | Purpose | State | Minimum gate |
|---|---|---|---|
| Intake | Submit documents, references, and intended-use metadata | Planned | auth, validation, malware/integrity controls |
| Source registry | Resolve authority, identity, versions, supersession, freshness | Planned | canonical registry and update policy |
| Evidence | Build and retrieve traceable evidence bundles | Planned | immutable lineage and access control |
| Assurance | Evaluate claims/documents and return bounded outcomes | Planned | policy versioning, evaluation, human-review rules |
| Modules | Discover and invoke stable MOUUK capabilities | Planned | canonical registry, routing tests, scopes |
| Agents | Register callers, tools, permissions, and actions | Deferred | identity, least privilege, durable audit |
| Audit | Retrieve authorized decision and lineage events | Deferred | privacy, retention, tamper evidence |

## Production response requirements

A future assurance response must include at least:

- assurance outcome and declared scope;
- evidence bundle reference and material citations;
- limitations and human-review requirement;
- source freshness/supersession state;
- gateway, module, rule/policy, and calibration versions;
- correlation ID and durable audit reference.

## Change rule

Update this register in the same pull request that adds, changes, deprecates, or removes a business route. Tests must compare registered routes with executable routes before production release.
