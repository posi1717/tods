from fastapi import FastAPI
from pydantic import BaseModel

from SKBUK.skbuk_calibrator import SKBUKCalibrator
from MOUUK.mouuk_01 import MOUUK01ProcurementAct
from tods_gateway.api import router as tods_gateway_router


app = FastAPI(
    title="TODS Gateway",
    version="1.1.0",
    description=(
        "UK procurement evidence gateway: "
        "SKBUK evidence -> MOUUK specialist modules -> TODS calibration."
    ),
)

app.include_router(tods_gateway_router)

calibrator = SKBUKCalibrator()
mouuk_01 = MOUUK01ProcurementAct()


class RegulatoryInput(BaseModel):
    content: str
    source: str = "UK Government"


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "TODS Gateway is running successfully",
        "architecture": "SKBUK -> MOUUK 1-34 -> TODS calibration",
        "api_version": app.version,
    }


@app.post("/api/v1/process-regulation")
def process_regulation(data: RegulatoryInput):
    """
    Legacy two-layer pipeline retained for backward compatibility.

    New TODS Gateway routes:
    - GET /health
    - GET /api/v1/tods-gateway/modules
    - POST /api/v1/tods-gateway/calibrate
    """
    calibration_result = calibrator.calibrate(data.model_dump())

    if not calibration_result["is_passed"]:
        return {
            "status": "rejected_at_layer_1",
            "gateway_layer": "SKBUK",
            "calibration_details": calibration_result,
            "message": "Data failed regulatory calibration thresholds.",
        }

    target_module = calibration_result.get("target_mouuk_routing")

    if target_module == "MOUUK_01_ProcurementAct":
        module_output = mouuk_01.process(data.model_dump())
    else:
        module_output = {
            "module": target_module,
            "analysis_result": "PENDING_IMPLEMENTATION",
            "message": "Target MOUUK module structure is ready for expansion.",
        }

    return {
        "status": "success",
        "architecture_flow": {
            "layer_1_skbuk": calibration_result,
            "layer_2_mouuk": module_output,
        },
    }