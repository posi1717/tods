# Configuration Precedence

**Status:** Active  
**Verified:** 24 September 2026

## Current collector behavior

The collector CLI accepts `--config PATH`; when omitted it resolves `config.yaml` from the current working directory. `uk_kb_collector.config.load_config` reads that single YAML file and applies in-code defaults only for optional keys.

Runtime precedence is therefore:

1. command-line mode override: `--dry-run` or `--production`;
2. values in the YAML file selected by `--config` (default: root `config.yaml`);
3. defaults coded in `uk_kb_collector/config.py` for omitted optional values.

The two mode flags are mutually exclusive. They override only `collector.dry_run`; they do not merge a second configuration file.

## Root configuration files

| File | Current runtime status | Required treatment |
|---|---|---|
| `config.yaml` | Active collector configuration by default | Treat as the current operational source for collector, compliance, allowed-domain, source, keyword, and category settings. |
| `sources.yml` | Not loaded by the current collector CLI/config loader | Treat as a proposed normalized source registry until an explicit loader, schema, tests, and migration path are implemented. |
| `classification.yml` | Not loaded by the current collector CLI/config loader | Treat as a proposed classification-rule registry until it is integrated and tested. |
| `uk_kb_collector/modules.yaml` | Canonical MOUUK module catalogue | Load only through `ModuleRegistry`; do not duplicate its 34 definitions in another editable registry. |
| Environment variables | No collector override contract is implemented | Do not document environment precedence unless code and tests add it. Secrets may still be supplied to unrelated tooling, but must not be committed. |

## Known conflict

`config.yaml` and `sources.yml` contain overlapping source definitions with different field names and non-identical lists. Because only `config.yaml` is loaded at runtime, editing `sources.yml` currently does not change collector behavior. Presenting both files as active would create a false source of truth.

`classification.yml` describes a structured rule vocabulary, while the current collector receives keywords and categories from `config.yaml`. Its presence does not prove those classification rules are executed.

## Integration gate

Before promoting `sources.yml` or `classification.yml` to canonical runtime inputs:

1. define versioned schemas and validation errors;
2. choose whether the files replace or are merged with sections of `config.yaml`;
3. specify deterministic precedence and duplicate/conflict handling;
4. add tests for missing, malformed, duplicate, disabled, and conflicting records;
5. migrate existing values without silently dropping sources or classification behavior;
6. update collector operations and the canonical document register in the same change.

Until then, `config.yaml` remains the current runtime configuration and the other two files are reference/proposed inputs.
