import json

from skbuk.services.delivery import MODULE_CODES, publish_references


def test_delivery_publishes_all_manifests_and_only_references(tmp_path):
    assert publish_references(tmp_path, [{
        "source_id": "src_procurement_act_2023",
        "source_url": "https://www.legislation.gov.uk/act.pdf",
        "sha256": "a" * 64,
        "storage_path": "01_OFFICIAL_SOURCES/act.pdf",
    }]) == 34

    assert len(list((tmp_path / "delivery" / "MOUUK").glob("*.json"))) == len(MODULE_CODES)
    payload = json.loads((tmp_path / "delivery" / "MOUUK" / "MOUUK-0001.json").read_text())
    assert payload["documents"][0]["storage_path"] == "01_OFFICIAL_SOURCES/act.pdf"
    assert "pdf_content" not in payload["documents"][0]
