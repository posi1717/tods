import httpx

from skbuk.repositories.supabase_registry import SupabaseRegistry


def test_healthcheck_uses_protected_registry_table_and_service_headers():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/rest/v1/tod_ingestion_runs"
        assert request.url.params["select"] == "run_id"
        assert request.url.params["limit"] == "1"
        assert request.headers["apikey"] == "test-key"
        assert request.headers["authorization"] == "Bearer " + "test-key"
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
