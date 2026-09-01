from pathlib import Path

import httpx

from skbuk.services.collection import collect


def _config(path: Path) -> Path:
    path.write_text(
        """sources:
  - source_id: guidance
    source_name: Guidance
    landing_url: https://www.gov.uk/collection
    publisher: gov.uk
    enabled: true
""",
        encoding="utf-8",
    )
    return path


def test_collection_stores_valid_official_pdf_and_reports(tmp_path: Path):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        if request.url.path == "/collection":
            return httpx.Response(200, text='<a href="/guide.pdf">Guide</a>')
        if request.url.path == "/guide.pdf":
            return httpx.Response(200, headers={"content-type": "application/pdf"}, content=b"%PDF-1.7\n")
        raise AssertionError(request.url)

    result = collect(_config(tmp_path / "sources.yaml"), tmp_path / "data", "SKBUK", 1000, 1, client=httpx.Client(transport=httpx.MockTransport(handler)))

    assert result.stored == 1
    assert result.discovered == 1
    assert list((tmp_path / "data" / "01_OFFICIAL_SOURCES" / "guidance").glob("*.pdf"))
    assert result.report_path.is_file()


def test_collection_does_not_store_when_robots_disallows(tmp_path: Path):
    client = httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200, text="User-agent: *\nDisallow: /")))

    result = collect(_config(tmp_path / "sources.yaml"), tmp_path / "data", "SKBUK", 1000, 1, client=client)

    assert result.sources_checked == 1
    assert result.discovered == 0
    assert result.rejected == 1
    assert result.stored == 0
    assert not (tmp_path / "data" / "01_OFFICIAL_SOURCES").exists()


def test_dry_run_reports_would_store_without_writing(tmp_path: Path):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        if request.url.path == "/collection":
            return httpx.Response(200, text='<a href="/guide.pdf">Guide</a>')
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=b"%PDF-1.7\n")

    result = collect(_config(tmp_path / "sources.yaml"), tmp_path / "data", "SKBUK", 1000, 1, True, httpx.Client(transport=httpx.MockTransport(handler)))

    assert result.stored == 0
    assert result.would_store == 1
    assert not (tmp_path / "data" / "01_OFFICIAL_SOURCES").exists()
