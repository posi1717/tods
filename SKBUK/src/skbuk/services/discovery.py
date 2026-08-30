from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup


def discover_links(client: httpx.Client, landing_url: str) -> list[str]:
    response = client.get(landing_url, follow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return sorted({urljoin(landing_url, tag.get("href")) for tag in soup.select("a[href]") if tag.get("href", "").lower().split("?", 1)[0].endswith((".pdf", ".html", ".htm"))})
