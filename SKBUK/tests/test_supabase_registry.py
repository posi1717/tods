import httpx

from skbuk.repositories.supabase_registry import SupabaseRegistry


def test_healthcheck_uses_protected_registry_table_and_service_headers():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/rest/v1/tod_ingestion_runs"
        assert request.url.params["select"] == "run_id"
        assert request.url.params["limit"] == "1"
        assert request.headers["apikey"] == "test-key"
        assert request.headers["Authorization"] == "Bearer " + "test-key"
        return httpx.Response(200, json=[])

    registry = SupabaseRegistry(
        httpx.Client(transport=httpx.MockTransport(handler)),
        "https://project.supabase.co/",
        "test-key",
    )

    assert registry.healthcheck()


def test_insert_uses_supabase_rest_without_storage_metadata_access():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/rest/v1/tod_ingestion_events"
        assert request.content == b'{"event_type":"test"}'
        return httpx.Response(201, json=[{"event_id": "1"}])

    registry = SupabaseRegistry(
        httpx.Client(transport=httpx.MockTransport(handler)),
        "https://project.supabase.co",
        "test-key",
    )

    assert registry.insert("tod_ingestion_events", {"event_type": "test"}) == [{"event_id": "1"}]


def test_healthcheck_returns_false_without_supabase_url():
    registry = SupabaseRegistry(httpx.Client(), None, "test-key")

    assert not registry.healthcheck()


def test_upload_writes_pdf_to_private_official_bucket():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/storage/v1/object/tod-official/01_OFFICIAL_SOURCES/a.pdf"
        assert request.headers["Content-Type"] == "application/pdf"
        assert request.headers["x-upsert"] == "false"
        assert request.content == b"%PDF-1.7\n"
        return httpx.Response(200)

    registry = SupabaseRegistry(
        httpx.Client(transport=httpx.MockTransport(handler)),
        "https://project.supabase.co",
        "test-key",
    )

    registry.upload_official_pdf("01_OFFICIAL_SOURCES/a.pdf", b"%PDF-1.7\n")
