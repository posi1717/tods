from pathlib import Path
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from skbuk.services.hasher import sha256_file
from skbuk.services.validator import validate_pdf


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)
def download_pdf(client: httpx.Client, url: str, target: Path, max_bytes: int) -> tuple[int, str, str]:
    with client.stream("GET", url, follow_redirects=True) as response:
        response.raise_for_status()
        total = 0
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("wb") as stream:
            for chunk in response.iter_bytes():
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("download exceeds configured size limit")
                stream.write(chunk)
        validate_pdf(target, response.headers.get("content-type", ""), max_bytes)
        return response.status_code, response.headers.get("etag", ""), sha256_file(target)
