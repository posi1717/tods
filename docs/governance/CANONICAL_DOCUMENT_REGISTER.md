# Canonical Document Register

Status: **CANONICAL**  
Owner: TODS Gateway maintainers

This register identifies which documents define the current system. A document not listed as canonical may still be valuable, but it cannot override the sources below.

## Precedence

When documents conflict, use this order:

1. executable code, database migrations, and passing tests for current behavior;
2. this register and the canonical architecture record for intended boundaries;
3. versioned schemas and machine-readable registries;
4. active operations documentation;
5. reference and historical material.

A conflict between executable behavior and the intended architecture is a tracked gap—not permission to silently rewrite either side.

## Register

| Document/source | Status | Authority |
|---|---|---|
| `docs/architecture/TODS_GATEWAY_ARCHITECTURE_RECORD.md` | Canonical | Product identity, trust boundary, components, assurance model |
| `uk_kb_collector/modules.yaml` | Canonical machine-readable | Stable MOUUK IDs, slugs, names, relationships, kinds |
| `docs/MOUUK_MODULE_CATALOGUE.md` | Canonical human-readable | Explanatory MOUUK module catalogue; must agree with YAML |
| `docs/REGISTRY_SCHEMA.md` | Canonical | File-based registry fields and storage contract |
| `docs/governance/DATA_GOVERNANCE_AND_LIFECYCLE.md` | Canonical | Database schema status, lineage, access, retention, and reconciliation rules |
| `docs/governance/CONFIGURATION_PRECEDENCE.md` | Canonical operational | Active collector configuration order and non-runtime reference files |
| `supabase/migrations/**` | Canonical migration history | Forward-only Supabase deployment history; do not rewrite applied migrations |
| `docs/operations/API_DEPLOYMENT_REGISTER.md` | Canonical operational | Executable and planned API status |
| `docs/MASTER_CHANGE_LIST.md` | Active control | Ordered, reversible implementation work |
| `README.md` | Active entry point | Project overview, current baseline, navigation |
| `SKBUK_ARCHITECTURE.md` | Active subsystem | SKBUK architecture, pending alignment review |
| `SKBUK/sql/**` | Active design | SKBUK package schema/storage design; not deployed until promoted through migrations |
| `docs/operations/COLLECTOR_OPERATIONS.md` | Active operational | Safe collector execution guidance |
| `docs/MOUUK_MODULE_CATALOGUE.pdf` | Generated/reference | Distribution rendering; Markdown is editable source |
| `sources.yml` | Proposed/reference | Normalized source registry not loaded by the current collector runtime |
| `classification.yml` | Proposed/reference | Classification-rule registry not loaded by the current collector runtime |
| `project_info__*.md` | Pending classification | Historical/working notes until reviewed |
| `docs/archive/**` | Archive | Historical context only; never current authority |

## Status labels

- **CANONICAL**: approved source of truth within its declared scope.
- **ACTIVE**: maintained operational or explanatory document.
- **REFERENCE**: useful supporting information, not authoritative.
- **GENERATED**: derived from a canonical source and not edited independently.
- **ARCHIVE**: retained history that must not guide current operation without revalidation.
- **PLANNED**: approved direction not yet implemented.

## Change control

Changes to canonical architecture, module identity, schema, API contract, assurance outcomes, or deployment gates require:

1. a pull request with the reason and affected scope;
2. review against code, tests, migrations, and downstream consumers;
3. corresponding tests or an explicit explanation when not testable;
4. update of this register when authority or path changes;
5. no silent replacement of a stable ID or historical record.

## Archive policy

Archive movement must use a dedicated commit so history remains reviewable. Archived documents receive a banner stating that they are non-canonical and naming the current replacement where one exists. Runtime data and evidence are governed by retention policy and are not treated as ordinary documentation cleanup.
