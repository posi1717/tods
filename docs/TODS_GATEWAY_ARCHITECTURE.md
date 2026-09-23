# TODS Gateway

TODS Gateway is the verified knowledge boundary for the TODS ecosystem.

- **SKBUK** discovers, validates, hashes, versions and classifies official UK procurement sources.
- **MOUUK-0001 to MOUUK-0034** are specialist interpretation modules.
- **Calibration Gate** blocks claims unless cited SKBUK evidence, authority level, confidence and evidence fingerprint pass deterministic checks.
- **Consumers** such as TGOS and Doccute receive auditable outputs rather than ungrounded AI answers.

## Operating Rule

MOUUK modules must not publish a claim without an `EvidenceBundle` produced from SKBUK-controlled sources. Every output identifies the cited document versions and evidence fingerprint used during calibration.

## Phase-One Foundation

This foundation provides:

1. Shared Pydantic contracts for evidence bundles and knowledge claims.
2. A declarative registry for 34 MOUUK specialist modules.
3. Deterministic calibration checks.
4. A small orchestration service ready to connect to FastAPI and Supabase.

## Next Steps

1. Connect SKBUK collector records to `EvidenceItem`.
2. Map detailed MOUUK specifications into the module registry.
3. Add approved evaluation cases per module.
4. Persist evidence, claims and append-only audit events in Supabase.
5. Expose versioned Gateway endpoints to TGOS and Doccute.
