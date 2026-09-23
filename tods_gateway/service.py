"""TODS Gateway orchestration service."""

from __future__ import annotations

from .calibration import calibrate_claim
from .models import EvidenceBundle, KnowledgeClaim
from .modules import get_module


def submit_claim_for_calibration(
    claim: KnowledgeClaim,
    evidence: EvidenceBundle,
) -> KnowledgeClaim:
    get_module(claim.module_id)
    result = calibrate_claim(claim, evidence)
    return claim.model_copy(update={"calibration_status": result.status})


def gateway_health() -> dict[str, object]:
    return {
        "service": "TODS Gateway",
        "source_layer": "SKBUK",
        "specialist_modules": 34,
        "calibration_required": True,
        "status": "ok",
    }
