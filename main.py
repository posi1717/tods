from fastapi import FastAPI
from pydantic import BaseModel

from MOUUK.mouuk_01 import MOUUK01ProcurementAct
from SKBUK.skbuk_calibrator import SKBUKCalibrator

app = FastAPI(
    title="TODS Gateway",
    version="1.0.0",
    description=(
        "Regulatory and document assurance gateway for public-service workflows. "
        "The current baseline is experimental and requires human review."
    ),
)

calibrator = SKBUKCalibrator()
mouuk_01 = MOUUK01ProcurementAct()


class RegulatoryInput(BaseModel):
    content: str
    source: str = "UK Government"


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "TODS Gateway",
        "role": "regulatory_and_document_assurance_gateway",
        "architecture": "TODS Gateway -> SKBUK -> MOUUK",
        "assurance_level": "experimental_human_review_required",
    }


@app.post("/api/v1/process-regulation")
def process_regulation(data: RegulatoryInput):
    """Run the initial SKBUK calibration and MOUUK specialist-routing path.

    This baseline does not issue production-grade assurance. Consequential use
    requires evidence validation and accountable human review.
    """
    payload = data.model_dump()
    calibration_result = calibrator.calibrate(payload)

    if not calibration_result["is_passed"]:
        return {
            "status": "INSUFFICIENT_EVIDENCE",
            "gateway_layer": "SKBUK",
            "calibration_details": calibration_result,
            "requires_human_review": True,
            "message": "Input failed the baseline calibration threshold.",
        }

    target_module = calibration_result.get("target_mouuk_routing")
    if target_module == "MOUUK_01_ProcurementAct":
        module_output = mouuk_01.process(payload)
    else:
        module_output = {
            "module": target_module,
            "analysis_result": "PENDING_IMPLEMENTATION",
            "message": "The target MOUUK route is not yet implemented in this gateway path.",
        }

    return {
        "status": "NEEDS_HUMAN_REVIEW",
        "requires_human_review": True,
        "architecture_flow": {
            "layer_1_skbuk": calibration_result,
            "layer_2_mouuk": module_output,
        },
    }
