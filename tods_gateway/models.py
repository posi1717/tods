"""
TODS Gateway shared contracts.

SKBUK supplies verified, versioned official-source evidence.
MOUUK specialist modules may only produce knowledge claims from an EvidenceBundle.
TODS Gateway exposes calibrated, auditable outputs to TGOS, Doccute and other consumers.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl, field_validator


class AuthorityLevel(str, Enum):
    PRIMARY_LAW = "primary_law"
    SECONDARY_LEGISLATION = "secondary_legislation"
    OFFICIAL_GUIDANCE = "official_guidance"
    POLICY_NOTICE = "policy_notice"
    OFFICIAL_PLATFORM = "official_platform"


class CalibrationStatus(str, Enum):
    DRAFT = "draft"
    PROVISIONAL = "provisional"
    CALIBRATED = "calibrated"
    BLOCKED = "blocked"


class EvidenceItem(BaseModel):
    document_id: str = Field(min_length=3, max_length=160)
    version_id: str = Field(min_length=3, max_length=200)
    source_url: HttpUrl
    publisher: str = Field(min_length=2, max_length=160)
    authority: AuthorityLevel
    title: str = Field(min_length=3, max_length=500)
    retrieved_at: datetime
    published_at: datetime | None = None
    effective_from: datetime | None = None
    excerpt: str = Field(min_length=1, max_length=12000)
    passage_reference: str | None = Field(default=None, max_length=300)
    checksum_sha256: str = Field(min_length=64, max_length=64)

    @field_validator("checksum_sha256")
    @classmethod
    def validate_checksum(cls, value: str) -> str:
        value = value.lower()
        if any(char not in "0123456789abcdef" for char in value):
            raise ValueError("checksum_sha256 must be hexadecimal")
        return value


class EvidenceBundle(BaseModel):
    bundle_id: str = Field(default_factory=lambda: f"evb_{uuid4().hex}")
    query: str = Field(min_length=3, max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    items: list[EvidenceItem] = Field(min_length=1)
    source_layer: Literal["SKBUK"] = "SKBUK"

    @property
    def evidence_fingerprint(self) -> str:
        raw = "|".join(
            f"{item.document_id}:{item.version_id}:{item.checksum_sha256}"
            for item in sorted(self.items, key=lambda item: item.document_id)
        )
        return sha256(raw.encode("utf-8")).hexdigest()


class KnowledgeClaim(BaseModel):
    claim_id: str = Field(default_factory=lambda: f"clm_{uuid4().hex}")
    module_id: str = Field(pattern=r"^MOUUK-\d{4}$")
    statement: str = Field(min_length=10, max_length=4000)
    evidence_document_ids: list[str] = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    limitations: list[str] = Field(default_factory=list)
    calibration_status: CalibrationStatus = CalibrationStatus.DRAFT
    evidence_fingerprint: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CalibrationResult(BaseModel):
    passed: bool
    status: CalibrationStatus
    score: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
