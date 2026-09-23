"""Deterministic calibration rules for TODS Gateway knowledge claims."""

from __future__ import annotations

from .models import AuthorityLevel, CalibrationResult, CalibrationStatus, EvidenceBundle, KnowledgeClaim
from .modules import get_module


MINIMUM_CALIBRATED_CONFIDENCE = 0.70


def calibrate_claim(claim: KnowledgeClaim, evidence: EvidenceBundle) -> CalibrationResult:
    reasons: list[str] = []
    module = get_module(claim.module_id)
    evidence_by_id = {item.document_id: item for item in evidence.items}

    missing = sorted(set(claim.evidence_document_ids) - set(evidence_by_id))
    if missing:
        reasons.append(f"Missing cited evidence documents: {', '.join(missing)}")

    if claim.evidence_fingerprint != evidence.evidence_fingerprint:
        reasons.append("Claim evidence fingerprint does not match the supplied SKBUK evidence bundle")

    if claim.confidence < MINIMUM_CALIBRATED_CONFIDENCE:
        reasons.append(
            f"Confidence {claim.confidence:.2f} is below calibrated threshold "
            f"{MINIMUM_CALIBRATED_CONFIDENCE:.2f}"
        )

    allowed_authorities = set(module.minimum_authorities)
    cited_items = [
        evidence_by_id[item_id]
        for item_id in claim.evidence_document_ids
        if item_id in evidence_by_id
    ]
    if not cited_items:
        reasons.append("No valid cited evidence items are available")
    elif not any(item.authority in allowed_authorities for item in cited_items):
        reasons.append("Cited evidence authority is not permitted for this module")

    has_official_evidence = any(
        item.authority in {
            AuthorityLevel.PRIMARY_LAW,
            AuthorityLevel.SECONDARY_LEGISLATION,
            AuthorityLevel.OFFICIAL_GUIDANCE,
            AuthorityLevel.POLICY_NOTICE,
            AuthorityLevel.OFFICIAL_PLATFORM,
        }
        for item in cited_items
    )
    if not has_official_evidence:
        reasons.append("Claim lacks primary or official evidence")

    passed = not reasons
    return CalibrationResult(
        passed=passed,
        status=CalibrationStatus.CALIBRATED if passed else CalibrationStatus.BLOCKED,
        score=1.0 if passed else max(0.0, 1.0 - 0.2 * len(reasons)),
        reasons=reasons,
    )

