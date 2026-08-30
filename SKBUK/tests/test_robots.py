import httpx
from skbuk.services.robots import check


def test_unreadable_robots_is_rejected():
    client = httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(503)))
    result = check(client, "https://www.gov.uk/a.pdf", "SKBUK")
    assert result.status == "unreadable"
    assert not result.allowed


def test_disallowed_robots_is_rejected():
    client = httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200, text="User-agent: *\nDisallow: /")))
    result = check(client, "https://www.gov.uk/a.pdf", "SKBUK")
    assert result.status == "disallowed"
    assert not result.allowed
