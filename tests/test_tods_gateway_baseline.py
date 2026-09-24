from pathlib import Path

from main import app
from uk_kb_collector.core.module_registry import ModuleRegistry


def test_tods_business_routes_match_baseline_register():
    routes = {
        (method, route.path)
        for route in app.routes
        for method in getattr(route, "methods", set())
        if route.path not in {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
    }
    assert routes == {
        ("GET", "/"),
        ("POST", "/api/v1/process-regulation"),
    }


def test_gateway_uses_tods_identity():
    assert app.title == "TODS Gateway"
    assert "document assurance" in app.description.lower()


def test_canonical_documents_exist():
    root = Path(__file__).parents[1]
    required = {
        "docs/MASTER_CHANGE_LIST.md",
        "docs/architecture/TODS_GATEWAY_ARCHITECTURE_RECORD.md",
        "docs/governance/CANONICAL_DOCUMENT_REGISTER.md",
        "docs/operations/API_DEPLOYMENT_REGISTER.md",
        "docs/operations/COLLECTOR_OPERATIONS.md",
    }
    assert all((root / path).is_file() for path in required)


def test_canonical_registry_has_all_stable_modules():
    modules = list(ModuleRegistry.load())
    assert [module.code for module in modules] == [f"MOUUK-{number:04d}" for number in range(1, 35)]
