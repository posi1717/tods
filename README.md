# TODS Gateway

**TODS Gateway is the regulatory and document-assurance gateway for public-service work.** It is the first controlled entry point for people, products, and AI agents that need to use rules, guidance, evidence, documents, or reports—and the final assurance checkpoint before material outputs are relied upon.

TODS is designed to be direct about evidence. It must distinguish sourced facts from interpretation, expose uncertainty and limitations, retain provenance, and require human review when the available evidence cannot support a dependable answer.

## Mission

Every TODS-connected project should pass regulated questions, material documents, reports, and agent actions through a consistent assurance boundary:

1. Identify the caller, intended use, and applicable scope.
2. verify source authority, document identity, version, and freshness.
3. bind material claims to traceable evidence.
4. apply the appropriate specialist MOUUK module and policy controls.
5. return a clear assurance outcome, limitations, and audit reference.
6. require accountable human approval where risk or policy requires it.

TODS is not a substitute for legal advice or an accountable public authority. It is an evidence-first control and assurance system.

## Architecture

```text
Person / Product / AI Agent
             |
             v
+---------------------------------------------+
|                 TODS Gateway                |
| identity | scope | policy | audit | outcome |
+---------------------------------------------+
             |
       +-----+-----+
       |           |
       v           v
+-------------+  +----------------------------+
|    SKBUK    |  |           MOUUK            |
| acquisition |  | 34 specialist modules      |
| custody      |  | rules, analysis, evidence  |
| provenance   |  | and review requirements    |
| calibration  |  +----------------------------+
+-------------+
       |           |
       +-----+-----+
             v
 Evidence bundle -> claim -> assurance outcome -> audit record
```

- **TODS Gateway** is the control plane and common interface.
- **SKBUK** is the governed acquisition, custody, provenance, versioning, and initial calibration layer. The original UK public-sector procurement collector remains an essential subsystem here.
- **MOUUK** is the specialist knowledge and reasoning layer. Stable module identities are defined by `uk_kb_collector/modules.yaml` from `MOUUK-0001` through `MOUUK-0034`.

See [the architecture record](docs/architecture/TODS_GATEWAY_ARCHITECTURE_RECORD.md) for boundaries and trust rules.

## Current baseline

The repository currently contains two related implementation paths:

- `main.py` exposes the initial FastAPI gateway with `GET /` and `POST /api/v1/process-regulation`.
- `uk_kb_collector/` contains the mature collector, evidence/provenance contracts, the canonical 34-module registry, and independently loadable specialist workers.

The present gateway route performs keyword-based SKBUK calibration and implements direct specialist processing for MOUUK-0001. Other routes/modules must not be described as production assurance until their evidence, policy, tests, and audit controls satisfy the deployment gates.

## Assurance language

TODS documentation and APIs use these target outcomes:

- `VERIFIED`
- `VERIFIED_WITH_LIMITATIONS`
- `NEEDS_HUMAN_REVIEW`
- `INSUFFICIENT_EVIDENCE`
- `STALE_SOURCE_RISK`
- `OUT_OF_SCOPE`
- `BLOCKED`

The current baseline does **not** yet issue production-grade `VERIFIED` decisions. Until the required controls are implemented, consequential outputs must default to review rather than implied certainty.

## Repository map

```text
.
├── main.py                         # Initial FastAPI gateway
├── SKBUK/                          # SKBUK service/calibration implementation
├── MOUUK/                          # Early direct MOUUK integration
├── uk_kb_collector/                # Collector, contracts, modules, workers
├── Knowledge_Base/                 # Governed knowledge-base workspace
├── docs/
│   ├── architecture/               # Canonical system architecture
│   ├── governance/                 # Document and trust governance
│   ├── operations/                 # API and collector operations
│   └── archive/                    # Non-canonical historical notes
├── supabase/                       # Database migrations
└── tests/                          # Architecture, schema, and governance tests
```

## Install and test

Python 3.12 is used by CI.

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e "./SKBUK[test]"
python -m pytest -q
```

Run the initial gateway:

```bash
uvicorn main:app --reload
```

Run the collector in dry-run mode:

```bash
python -m uk_kb_collector.main --dry-run
```

See [collector operations](docs/operations/COLLECTOR_OPERATIONS.md) before running production collection.

## Canonical documents

- [Master change list](docs/MASTER_CHANGE_LIST.md)
- [Architecture record](docs/architecture/TODS_GATEWAY_ARCHITECTURE_RECORD.md)
- [Canonical document register](docs/governance/CANONICAL_DOCUMENT_REGISTER.md)
- [API deployment register](docs/operations/API_DEPLOYMENT_REGISTER.md)
- [MOUUK module catalogue](docs/MOUUK_MODULE_CATALOGUE.md)
- [Registry schema](docs/REGISTRY_SCHEMA.md)
- [SKBUK architecture](SKBUK_ARCHITECTURE.md)

## Change safety

This baseline preserves the collector, SKBUK, all 34 stable MOUUK identities, source manifests, migrations, evidence records, tests, and historical Git record. Runtime logs, temporary downloads, caches, credentials, and build artefacts must not be committed. Destructive cleanup requires a separate dependency and retention review.
