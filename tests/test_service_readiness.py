from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_service_packaging_files_exist():
    required = {"Dockerfile", "compose.yaml", ".dockerignore", "static/index.html", "static/styles.css", "static/app.js"}
    assert all((ROOT / path).is_file() for path in required)


def test_container_runs_as_non_root_user_and_healthchecks_status():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    compose = (ROOT / "compose.yaml").read_text(encoding="utf-8")

    assert "USER tods" in dockerfile
    assert "/api/v1/status" in compose


def test_service_readiness_does_not_claim_public_production():
    text = (ROOT / "docs/operations/SERVICE_READINESS.md").read_text(encoding="utf-8")

    assert "controlled internal demonstration or supervised pilot" in text
    assert "not approved for unsupervised public production assurance" in text
    assert "Authentication and scoped authorization are not implemented" in text
