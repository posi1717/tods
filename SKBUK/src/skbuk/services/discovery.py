from urllib.parse import urljoin
from html.parser import HTMLParser
import httpx


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def discover_links(client: httpx.Client, landing_url: str) -> list[str]:
    response = client.get(landing_url, follow_redirects=True)
    response.raise_for_status()
    parser = _LinkParser()
    parser.feed(response.text)
    return sorted({
        urljoin(landing_url, href)
        for href in parser.links
        if href.lower().split("?", 1)[0].endswith((".pdf", ".html", ".htm"))
    })
