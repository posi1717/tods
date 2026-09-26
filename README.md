# TODS Gateway

**TODS Gateway is the regulatory and document-assurance gateway for public-service work.** It is the first controlled entry point for people, products, and AI agents that need to use rules, guidance, evidence, documents, or reports—and the final assurance checkpoint before material outputs are relied upon.

TODS is designed to be direct about evidence. It distinguishes sourced facts from interpretation, exposes uncertainty and limitations, retains provenance, and requires human review when the available evidence cannot support a dependable answer.

## Public-procurement focus

TODS is focused initially on **trusted, evidence-based, and regulation-compliant documentation for public procurement**. Public procurement is more than an administrative process: it is one of the principal mechanisms through which governments invest public money, deliver essential services, build infrastructure, support markets, and pursue economic, environmental, and social outcomes.

London provides an unusually valuable real-world learning environment. Its public-service landscape brings together the Greater London Authority, 32 London boroughs, the City of London Corporation, Transport for London, NHS bodies, social and community housing providers, Net Zero programmes, and UK Government requirements. These institutions have different mandates, policies, procurement duties, and accountability structures, yet often need to work together for the same city and communities.

This environment has made the core problem clear: the challenge is not simply to produce more documents or introduce more AI. Important public-procurement documents must be trustworthy. Their sources should be authoritative, their evidence traceable, their regulatory context understood, their versions current, their limitations visible, and their final use accountable to a responsible person.

TODS is therefore being developed as an evidence-first assurance layer for public-procurement documents and regulated public-sector information. The aim is to give people, public organisations, digital services, and AI agents a common controlled process for checking provenance, applicable rules, document integrity, scope, uncertainty, and review requirements before information is relied upon.

## Trust in the AI era

Every country must consider how to preserve public trust as AI becomes involved in preparing, interpreting, and reviewing documents connected to public expenditure. If trustworthy, evidence-linked, and human-accountable documentation becomes part of the emerging global standard for public procurement in the AI era, TODS seeks to make a small but meaningful contribution to shaping that standard and the relationship of trust between technology, government, and people.

This work should not be developed in isolation. We welcome direct guidance and constructive challenge from specialists in public procurement, regulation, government documentation, AI governance, public administration, assurance, security, and responsible technology. Expert scrutiny can help test assumptions, identify missing safeguards, and ensure that the system develops in a genuinely useful and responsible direction.

We also welcome introductions to public bodies, research institutions, responsible technology partners, funders, and other supporters who share this purpose. Such connections could create opportunities to validate the approach, conduct carefully governed pilot projects, and determine where TODS can deliver measurable public value.

References to London institutions describe the regulatory and operational context from which the project learns; they do not imply endorsement, partnership, deployment, or approval by any named organisation.

## Enterprise console

The repository includes a responsive enterprise assurance console backed by the executable FastAPI service.

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e "./SKBUK[test]"
uvicorn main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/`. The UI can submit source-labelled material, display actual calibration/routing results, preserve a correlation ID, and export the decision-support record. Every consequential result remains explicitly subject to accountable human review.

Container start:

```bash
docker compose up --build
```

See [enterprise console operations](docs/operations/ENTERPRISE_CONSOLE_OPERATIONS.md) and [service readiness](docs/operations/SERVICE_READINESS.md) before deployment.

## Mission

Every TODS-connected project should pass regulated questions, material documents, reports, and agent actions through a consistent assurance boundary:

1. Identify the caller, intended use, and applicable scope.
2. Verify source authority, document identity, version, and freshness.
3. Bind material claims to traceable evidence.
4. Apply the appropriate specialist MOUUK module and policy controls.
5. Return a clear assurance outcome, limitations, and audit reference.
6. Require accountable human approval where risk or policy requires it.

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

## Current service baseline

- `GET /` serves the enterprise assurance console.
- `GET /api/v1/status` reports the current service capabilities and missing controls.
- `POST /api/v1/process-regulation` performs baseline SKBUK calibration and direct specialist processing for MOUUK-0001.
- `uk_kb_collector/` provides the collector, evidence/provenance contracts, canonical 34-module registry, and independently loadable specialist workers.

Other routes and modules must not be described as production assurance until their evidence, policy, authentication, tests, audit controls, and deployment gates are satisfied.

## Assurance language

TODS documentation and APIs use these target outcomes:

- `VERIFIED`
- `VERIFIED_WITH_LIMITATIONS`
- `NEEDS_HUMAN_REVIEW`
- `INSUFFICIENT_EVIDENCE`
- `STALE_SOURCE_RISK`
- `OUT_OF_SCOPE`
- `BLOCKED`

The current baseline does **not** issue production-grade `VERIFIED` decisions. Until the required controls are implemented, consequential outputs default to review rather than implied certainty.

## Repository map

```text
.
├── main.py                         # FastAPI gateway and console routes
├── static/                         # Enterprise console HTML, CSS, JavaScript
├── Dockerfile                      # Non-root service image
├── compose.yaml                    # Local/container service definition
├── SKBUK/                          # SKBUK service/calibration implementation
├── MOUUK/                          # Direct MOUUK integration
├── uk_kb_collector/                # Collector, contracts, modules, workers
├── Knowledge_Base/                 # Governed knowledge-base workspace
├── docs/
│   ├── architecture/               # Canonical system architecture
│   ├── governance/                 # Document and trust governance
│   ├── operations/                 # API, console, and collector operations
│   └── archive/                    # Non-canonical historical notes
├── supabase/                       # Database migration history
└── tests/                          # Runtime, architecture, schema, and governance tests
```

## Test

Python 3.12 is used by CI.

```bash
python -m pytest -q
```

The current branch passes 67 tests in a clean checkout with declared root and `SKBUK[test]` dependencies installed. The service console, status endpoint, and regulatory assessment path also pass a live local smoke test.

Run the collector in dry-run mode:

```bash
python -m uk_kb_collector.main --dry-run
```

See [collector operations](docs/operations/COLLECTOR_OPERATIONS.md) before running production collection.

## Canonical documents

- [Master change list](docs/MASTER_CHANGE_LIST.md)
- [Architecture record](docs/architecture/TODS_GATEWAY_ARCHITECTURE_RECORD.md)
- [Canonical document register](docs/governance/CANONICAL_DOCUMENT_REGISTER.md)
- [Data governance and lifecycle](docs/governance/DATA_GOVERNANCE_AND_LIFECYCLE.md)
- [Configuration precedence](docs/governance/CONFIGURATION_PRECEDENCE.md)
- [API deployment register](docs/operations/API_DEPLOYMENT_REGISTER.md)
- [Enterprise console operations](docs/operations/ENTERPRISE_CONSOLE_OPERATIONS.md)
- [Service readiness](docs/operations/SERVICE_READINESS.md)
- [MOUUK module catalogue](docs/MOUUK_MODULE_CATALOGUE.md)
- [Registry schema](docs/REGISTRY_SCHEMA.md)
- [SKBUK architecture](SKBUK_ARCHITECTURE.md)

## Change safety

This baseline preserves the collector, SKBUK, all 34 stable MOUUK identities, source manifests, migrations, evidence records, tests, and historical Git record. Runtime logs, temporary downloads, caches, credentials, and build artefacts must not be committed. Destructive cleanup requires a separate dependency and retention review.
