from skbuk.utils.urls import ASSET_HOST, is_official_host


def approve(url: str, landing_url: str | None = None) -> bool:
    return is_official_host(url, from_approved_landing=bool(landing_url and is_official_host(landing_url)))


def explain(url: str, landing_url: str | None = None) -> str | None:
    if approve(url, landing_url):
        return None
    return "host_not_allowlisted"
