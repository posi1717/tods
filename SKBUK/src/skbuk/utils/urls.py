from urllib.parse import urlparse

ALLOWED_ROOTS = ("gov.uk", "legislation.gov.uk")
ASSET_HOST = "assets.publishing.service.gov.uk"


def is_official_host(url: str, *, from_approved_landing: bool = False) -> bool:
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    if host == ASSET_HOST:
        return from_approved_landing
    return any(host == root or host.endswith("." + root) for root in ALLOWED_ROOTS)


def host(url: str) -> str:
    return (urlparse(url).hostname or "").lower()
