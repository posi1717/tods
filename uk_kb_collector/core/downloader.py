"""Downloader abstraction for future controlled ingestion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DownloadTask:
    url: str
    module_code: str


class Downloader:
    def queue(self, task: DownloadTask) -> str:
        return f"queued:{task.module_code}"
