from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from uk_kb_collector.core.module_registry import ModuleRegistry


client = TestClient(app)


def test_tods_business_routes_match_service_register():
    routes = {
        (method, route.path)
        for route in app.routes
        for method in getattr(route, "methods", set())
        if route.path not in {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
        and not route.path.startswith("/static")
    }
    assert routes == {
        ("GET", "/"),
        ("GET", "/api/v1/status"),
        ("POST", "/api/v1/process-regulation"),
    }


def test_gateway_uses_tods_identity():
    assert app.title == "TODS Gateway"
    assert "document assurance" in app.description.lower()


def test_enterprise_console_is_served():
    response = client.get("/")

    assert response.status_code == 200
    assert "TODS Gateway | Assurance Console" in response.text
    assert "/static/styles.css" in response.text


def test_status_is_truthful_about_baseline_controls():
    response = client.get("/api/v1/status")
    body = response.json()

    assert response.status_code == 200
    assert body["canonical_mouuk_modules"] == 34
    assert body["controls"]["human_review"] == "required"
    assert body["controls"]["authentication"] == "not_implemented"


def test_process_route_returns_traceable_review_result():
    response = client.post(
        "/api/v1/process-regulation",
        json={
            "source": "UK Government",
            "content": (
                "The contracting authority is preparing a public contract under the Procurement Act 2023. "
                "The procurement team must document conditions, award criteria, transparency notices and "
                "conflicts of interest before an accountable professional reviews the tender decision."
            ),
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "NEEDS_HUMAN_REVIEW"
    assert body["requires_human_review"] is True
    assert body["correlation_id"]
    assert body["architecture_flow"]["layer_1_skbuk"]["target_mouuk_routing"] == "MOUUK_01_ProcurementAct"


def test_canonical_documents_exist():
    root = Path(__file__).parents[1]
    required = {
        "docs/MASTER_CHANGE_LIST.md",
        "docs/architecture/TODS_GATEWAY_ARCHITECTURE_RECORD.md",
        "docs/governance/CANONICAL_DOCUMENT_REGISTER.md",
        "docs/governance/DATA_GOVERNANCE_AND_LIFECYCLE.md",
        "docs/operations/API_DEPLOYMENT_REGISTER.md",
        "docs/operations/COLLECTOR_OPERATIONS.md",
    }
    assert all((root / path).is_file() for path in required)


def test_canonical_registry_has_all_stable_modules():
    modules = list(ModuleRegistry.load())
    assert [module.code for module in modules] == [f"MOUUK-{number:04d}" for number in range(1, 35)]
