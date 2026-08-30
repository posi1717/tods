from dataclasses import dataclass
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
import httpx


@dataclass(frozen=True)
class RobotsResult:
    status: str
    allowed: bool
    detail: str = ""


def check(client: httpx.Client, url: str, user_agent: str) -> RobotsResult:
    robots_url = urljoin(url, "/robots.txt")
    try:
        response = client.get(robots_url)
        response.raise_for_status()
        parser = RobotFileParser()
        parser.parse(response.text.splitlines())
        allowed = parser.can_fetch(user_agent, url)
        return RobotsResult("allowed" if allowed else "disallowed", allowed)
    except (httpx.HTTPError, UnicodeError) as exc:
        return RobotsResult("unreadable", False, str(exc))
