"""Stable interfaces for authority, temporal, relationship and evidence analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ENGINE_CODES = {
    "authority": "MOUUK-0023",
    "temporal": "MOUUK-0024",
    "relationship": "MOUUK-0025",
    "evidence": "MOUUK-0026",
}


@dataclass(frozen=True)
class IntelligenceResult:
    engine_code: str
    facts: dict[str, Any]
    confidence: float


def evaluate(engine: str, facts: dict[str, Any], confidence: float = 1.0) -> IntelligenceResult:
    """Create a typed result while concrete engine rules are introduced incrementally."""
    if engine not in ENGINE_CODES:
        raise ValueError(f"unknown intelligence engine: {engine}")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    return IntelligenceResult(ENGINE_CODES[engine], facts, confidence)
