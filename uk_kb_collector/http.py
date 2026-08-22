from __future__ import annotations

import logging
import time
import urllib.robotparser
from collections import defaultdict
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import CollectorConfig

LOG = logging.getLogger(__name__)


class SafeHttpClient:
    def __init__(self, config: CollectorConfig) -> None:
        self.config = config
        self.session = requests.Session()
        retry = Retry(
            total=config.max_retries,
            connect=config.max_retries,
            read=config.max_retries,
            status=config.max_retries,
            backoff_factor=config.backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "HEAD"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({"User-Agent": config.user_agent, "Accept": "text/html,application/pdf,*/*;q=0.8"})
        self.last_request: dict[str, float] = defaultdict(float)
        self.robots: dict[str, urllib.robotparser.RobotFileParser] = {}

    def _throttle(self, url: str) -> None:
        host = (urlparse(url).hostname or "").lower()
        remaining = self.config.min_delay_per_domain - (time.monotonic() - self.last_request[host])
        if remaining > 0:
            time.sleep(remaining)
        self.last_request[host] = time.monotonic()

    def robots_allowed(self, url: str) -> bool:
        host = (urlparse(url).hostname or "").lower()
        if host not in self.robots:
            rp = urllib.robotparser.RobotFileParser()
            robots_url = f"https://{host}/robots.txt"
            rp.set_url(robots_url)
            try:
                self._throttle(robots_url)
                response = self.session.get(
                    robots_url,
                    timeout=(self.config.connect_timeout, self.config.read_timeout),
                    verify=self.config.verify_tls,
                    allow_redirects=True,
                )
                response.raise_for_status()
                rp.parse(response.text.splitlines())
                self.robots[host] = rp
            except Exception as exc:
                LOG.warning("robots.txt could not be read for %s: %s; refusing automated access", host, exc)
                return False
        return self.robots[host].can_fetch(self.config.user_agent, url)

    def get(self, url: str, **kwargs):
        self._throttle(url)
        return self.session.get(
            url,
            timeout=(self.config.connect_timeout, self.config.read_timeout),
            verify=self.config.verify_tls,
            allow_redirects=True,
            **kwargs,
        )

    @staticmethod
    def http_date_value(value: str) -> str:
        if not value:
            return ""
        try:
            return parsedate_to_datetime(value).isoformat()
        except Exception:
            return value
