from skbuk.services.allowlist import approve


def test_non_allowlisted_domain_is_rejected():
    assert not approve("https://example.com/file.pdf")


def test_asset_host_requires_approved_landing():
    assert approve("https://assets.publishing.service.gov.uk/a.pdf", "https://www.gov.uk/guidance/x")
    assert not approve("https://assets.publishing.service.gov.uk/a.pdf")
