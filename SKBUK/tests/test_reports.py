from skbuk.services.reporting import write_markdown


def test_report_contains_required_sections(tmp_path):
    path = write_markdown(tmp_path / "report.md", "run-1", {"Sources checked": ["src-1"], "Robots refusals": [], "Next actions": ["review"]})
    text = path.read_text(encoding="utf-8")
    assert "# SKBUK ingestion report: run-1" in text
    assert "## Sources checked" in text
    assert "## Next actions" in text
