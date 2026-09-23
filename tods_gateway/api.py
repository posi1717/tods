from fastapi import APIRouter
from pydantic import BaseModel

from .calibration import calibrate_claim
from .models import CalibrationResult, EvidenceBundle, KnowledgeClaim
from .modules import MOUUK_MODULES
from .service import gateway_health

router = APIRouter(tags=["TODS Gateway"])


class CalibrationRequest(BaseModel):
    evidence: EvidenceBundle
    claim: KnowledgeClaim


@router.get("/health")
def health() -> dict[str, object]:
    return gateway_health()


@router.get("/api/v1/tods-gateway/modules")
def list_modules() -> dict[str, object]:
    return {
        "count": len(MOUUK_MODULES),
        "modules": [
            {
                "module_id": module.module_id,
                "name": module.name,
                "purpose": module.purpose,
                "depends_on": list(module.depends_on),
                "minimum_authorities": [
                    authority.value for authority in module.minimum_authorities
                ],
            }
            for module in MOUUK_MODULES
        ],
    }


@router.post(
    "/api/v1/tods-gateway/calibrate",
    response_model=CalibrationResult,
)
def calibrate(payload: CalibrationRequest) -> CalibrationResult:
    return calibrate_claim(payload.claim, payload.evidence)