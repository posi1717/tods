import pytest
from skbuk.services.storage import BIDDER_BUCKET, OFFICIAL_BUCKET, bidder_path, official_path, tender_path


def test_storage_paths_are_separated():
    assert OFFICIAL_BUCKET != BIDDER_BUCKET
    assert official_path("01_OFFICIAL_SOURCES/01_PRIMARY_LEGISLATION/PROCUREMENT_ACT_2023/a.pdf").startswith("01_OFFICIAL_SOURCES/")
    assert bidder_path("org-1", "B01", "identity.pdf").startswith("02_BIDDER_EVIDENCE/")
    assert tender_path("t-1", "ITT", "itt.pdf").startswith("03_TENDER_WORKSPACES/")


def test_path_traversal_and_unknown_sections_rejected():
    with pytest.raises(ValueError):
        official_path("../outside.pdf")
    with pytest.raises(ValueError):
        tender_path("t-1", "UNKNOWN", "x.pdf")
