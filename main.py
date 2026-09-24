from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from MOUUK.mouuk_01 import MOUUK01ProcurementAct
from SKBUK.skbuk_calibrator import SKBUKCalibrator

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="TODS Gateway",
    version="1.1.0",
    description=(
        "Regulatory and document assurance gateway for public-service workflows. "
        "The current service baseline requires accountable human review."
    ),
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

calibrator = SKBUKCalibrator()
mouuk_01 = MOUUK01ProcurementAct()


class RegulatoryInput(BaseModel):
    content: str = Field(min_length=1, max_length=100_000)
    source: str = Field(default="UK Government", min_length=2, max_length=500)


@app.get("/", include_in_schema=False)
def enterprise_console():
    """Serve the enterprise assurance console."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/v1/status")
def service_status():
    """Return truthful, machine-readable service capability status."""
    return {
        "status": "online",
        "service": "TODS Gateway",
        "version": app.version,
        "environment": "baseline",
        "assurance_level": "experimental_human_review_required",
        "implemented_business_routes": 3,
        "canonical_mouuk_modules": 34,
        "direct_specialist_routes": ["MOUUK-0001"],
        "controls": {
            "source_calibration": "baseline",
            "human_review": "required",
            "durable_audit": "not_implemented",
            "authentication": "not_implemented",
        },
    }


@app.post("/api/v1/process-regulation")
def process_regulation(data: RegulatoryInput):
    """Run the initial SKBUK calibration and MOUUK specialist-routing path.

    This baseline does not issue production-grade assurance. Consequential use
    requires evidence validation and accountable human review.
    """
    correlation_id = str(uuid4())
    payload = data.model_dump()
    calibration_result = calibrator.calibrate(payload)

    if not calibration_result["is_passed"]:
        return {
            "correlation_id": correlation_id,
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
        "correlation_id": correlation_id,
        "status": "NEEDS_HUMAN_REVIEW",
        "requires_human_review": True,
        "source": data.source,
        "architecture_flow": {
            "layer_1_skbuk": calibration_result,
            "layer_2_mouuk": module_output,
        },
    }
