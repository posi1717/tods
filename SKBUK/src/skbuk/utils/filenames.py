import re
from pathlib import PurePosixPath

_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def safe_segment(value: str, max_length: int = 120) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(" .-")[:max_length]
    return ("_" + value) if value.upper() in _RESERVED else (value or "unclassified")


def official_filename(date: str, publisher: str, title: str, version: int, sha256: str) -> str:
    return f"{safe_segment(date, 10)}__{safe_segment(publisher)}__{safe_segment(title)}__v{version}__{sha256[:8].upper()}.pdf"


def ensure_relative(path: str, prefix: str) -> str:
    normal = PurePosixPath(path.replace("\\", "/"))
    if normal.is_absolute() or ".." in normal.parts or not str(normal).startswith(prefix):
        raise ValueError(f"path must remain under {prefix}")
    return normal.as_posix()
