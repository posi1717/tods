"""API contract and reusable mechanics for independent reasoning workers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ReasoningRequest:
    question: str
    evidence: list[dict[str, Any]] = field(default_factory=list)
    as_of: str | None = None


@dataclass(frozen=True)
class ReasoningResponse:
    module_code: str
    module_name: str
    answer: str
    reasoning: list[str]
    citations: list[str]
    confidence: float
    needs_review: bool


class ReasoningWorker:
    """Base API implemented by every MOUUK knowledge/reasoning plugin."""

    def __init__(self, plugin_dir: Path) -> None:
        self.plugin_dir = plugin_dir
        self.manifest = self._read("module.yaml") or self._read("manifest.yaml")
        self.sources = self._read("sources.yaml")
        self.rules = self._read("rules.yaml")
        self.taxonomy = self._read("taxonomy.yaml")
        self.module_code = self.manifest["code"]
        self.module_name = self.manifest["name"]

    def healthcheck(self) -> str:
        return "ready"

    def _read(self, filename: str) -> dict[str, Any]:
        file_path = self.plugin_dir / filename
        if not file_path.exists():
            return {}
        return yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}

    def reason(self, request: ReasoningRequest) -> ReasoningResponse:
        """Evidence-first baseline; specialist workers may override this method."""
        evidence = [item for item in request.evidence if item.get("text")]
        citations = [item["url"] for item in evidence if item.get("url")]
        principles = self.rules.get("principles", [])
        steps = [f"Apply specialist scope: {self.manifest['expertise']}"]
        steps.extend(principles)
        if request.as_of:
            steps.append(f"Assess authority and currency as at {request.as_of}")
        if not evidence:
            return ReasoningResponse(
                self.module_code, self.module_name,
                "Insufficient evidence to provide a reliable specialist conclusion.",
                steps, [], 0.0, True,
            )
        summary = " ".join(item["text"].strip() for item in evidence)[:2000]
        return ReasoningResponse(
            self.module_code, self.module_name, summary, steps,
            list(dict.fromkeys(citations)), min(0.95, 0.55 + 0.1 * len(evidence)), False,
        )
