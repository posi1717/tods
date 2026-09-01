from skbuk.services.provenance import ProvenanceWriter


class FakeRegistry:
    def __init__(self):
        self.calls = []

    def insert(self, table, payload):
        self.calls.append((table, payload))
        return [{"run_id": "00000000-0000-0000-0000-000000000001"}]

    def upload_official_pdf(self, storage_path, content):
        self.calls.append(("upload", {"storage_path": storage_path, "content": content}))


def test_provenance_writes_run_and_reference_only_events():
    registry = FakeRegistry()
    writer = ProvenanceWriter(registry)

    writer.start()
    writer.accepted_document("source-1", "https://www.gov.uk/a.pdf", "a" * 64, "01_OFFICIAL_SOURCES/a.pdf")
    writer.finish("completed", {"stored": 1})

    assert [table for table, _ in registry.calls] == [
        "tod_ingestion_runs", "tod_ingestion_events", "tod_ingestion_events",
    ]
    document_event = registry.calls[1][1]
    assert document_event["payload"]["storage_path"] == "01_OFFICIAL_SOURCES/a.pdf"
    assert "pdf_content" not in document_event["payload"]


def test_provenance_marks_started_run_as_failed_when_collection_setup_fails(tmp_path):
    registry = FakeRegistry()
    from skbuk.services.collection import collect

    result = collect(
        tmp_path / "missing.yaml",
        tmp_path / "data",
        "SKBUK",
        1000,
        1,
        provenance=ProvenanceWriter(registry),
    )

    assert result.errors == 1
    assert registry.calls[-1][1]["payload"]["status"] == "failed"
