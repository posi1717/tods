from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Annotated, Self
from urllib.parse import urlparse

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, StringConstraints, field_validator, model_validator


Identifier = Annotated[str, StringConstraints(min_length=3, max_length=220, pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")]
Slug = Annotated[str, StringConstraints(min_length=3, max_length=180, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")]
Sha256 = Annotated[str, StringConstraints(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$")]


class Publisher(StrEnum):
    GOV_UK = "gov.uk"
    LEGISLATION_GOV_UK = "legislation.gov.uk"


class DocumentFamily(StrEnum):
    PRIMARY_LEGISLATION = "primary-legislation"
    SECONDARY_LEGISLATION = "secondary-legislation"
    EXPLANATORY_NOTES = "explanatory-notes"
    GUIDANCE = "guidance"
    POLICY_NOTES = "policy-notes"
    SUPPLIER_GUIDANCE = "supplier-guidance"
    TRAINING_MANUAL = "training-manual"
    CONSULTATION = "consultation"
    MISC = "misc"


class DocumentType(StrEnum):
    PDF = "pdf"


class Jurisdiction(StrEnum):
    UK = "UK"
    ENGLAND = "England"
    WALES = "Wales"
    SCOTLAND = "Scotland"
    NORTHERN_IRELAND = "Northern Ireland"


class Applicability(StrEnum):
    PUBLIC_PROCUREMENT = "public-procurement"
    PROCUREMENT_ACT_2023 = "procurement-act-2023"
    SUPPLIER_GUIDANCE = "supplier-guidance"
    CONTRACTING_AUTHORITIES = "contracting-authorities"
    CROSS_SECTOR = "cross-sector"


class LifecycleStatus(StrEnum):
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    MISSING = "missing"
    REJECTED = "rejected"


class RunStatus(StrEnum):
    COMPLETED = "completed"
    RUNNING = "running"
    FAILED = "failed"
    PARTIAL = "partial"


class RejectionReason(StrEnum):
    ROBOTS_UNREADABLE = "robots_unreadable"
    ROBOTS_DISALLOWED = "robots_disallowed"
    HOST_NOT_ALLOWLISTED = "host_not_allowlisted"
    NOT_PDF = "not_pdf"
    HTTP_ERROR = "http_error"
    INVALID_CONTENT_TYPE = "invalid_content_type"
    DUPLICATE_HASH = "duplicate_hash"
    FETCH_FAILED = "fetch_failed"
    CLASSIFICATION_FAILED = "classification_failed"
    PATH_POLICY_BLOCKED = "path_policy_blocked"


class SchemaModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, use_enum_values=True)


class Source(SchemaModel):
    source_id: Identifier
    source_name: str = Field(min_length=3, max_length=300)
    landing_url: AnyHttpUrl
    publisher: Publisher
    jurisdiction: Jurisdiction | None = Jurisdiction.UK
    category_hint: DocumentFamily | None = None
    enabled: bool = True
    robots_status: str = Field(pattern=r"^(allowed|disallowed|unreadable|unknown)$", default="unknown")
    last_robots_checked_at: datetime | None = None
    notes: str | None = Field(default=None, max_length=4000)

    @field_validator("last_robots_checked_at")
    @classmethod
    def require_utc(cls, value: datetime | None) -> datetime | None:
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("Datetime must be timezone-aware.")
        return value.astimezone(UTC) if value else None


class Run(SchemaModel):
    run_id: Identifier
    started_at: datetime
    finished_at: datetime | None = None
    status: RunStatus
    app_version: str = Field(min_length=1, max_length=50)
    source_count: int = Field(ge=0)
    discovered_count: int = Field(ge=0)
    downloaded_count: int = Field(ge=0)
    unchanged_count: int = Field(ge=0)
    rejected_count: int = Field(ge=0)
    error_count: int = Field(ge=0)
    report_path: str | None = None
    log_path: str | None = None

    @field_validator("started_at", "finished_at")
    @classmethod
    def require_utc(cls, value: datetime | None) -> datetime | None:
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("Datetime must be timezone-aware.")
        return value.astimezone(UTC) if value else None

    @model_validator(mode="after")
    def validate_timing(self) -> Self:
        if self.finished_at and self.finished_at < self.started_at:
            raise ValueError("finished_at cannot be earlier than started_at.")
        return self


class DocumentVersion(SchemaModel):
    version_id: Identifier
    document_id: Identifier
    run_id: Identifier
    download_url: AnyHttpUrl
    http_status: int = Field(ge=200, le=599)
    content_type: str = Field(min_length=3, max_length=150)
    content_length: int | None = Field(default=None, ge=1)
    etag: str | None = Field(default=None, max_length=500)
    last_modified: str | None = Field(default=None, max_length=200)
    sha256: Sha256
    file_name_original: str | None = Field(default=None, min_length=5, max_length=255)
    file_path_current: str
    file_path_versioned: str
    discovered_at: datetime
    downloaded_at: datetime
    is_binary_changed: bool
    change_reason: str | None = Field(default=None, max_length=200)
    version_label: str | None = Field(default=None, max_length=100)

    @field_validator("discovered_at", "downloaded_at")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must be timezone-aware.")
        return value.astimezone(UTC)

    @field_validator("file_path_current", "file_path_versioned")
    @classmethod
    def validate_relative_pdf_path(cls, value: str) -> str:
        path = PurePosixPath(value.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts or not str(path).startswith("data/documents/"):
            raise ValueError("Document paths must be relative and start with data/documents/.")
        if path.suffix.lower() != ".pdf":
            raise ValueError("Document paths must point to a PDF file.")
        return path.as_posix()

    @field_validator("content_type")
    @classmethod
    def require_pdf_content_type(cls, value: str) -> str:
        normalised = value.lower().split(";", maxsplit=1)[0].strip()
        if normalised != "application/pdf":
            raise ValueError("content_type must be application/pdf.")
        return normalised


class Document(SchemaModel):
    document_id: Identifier
    canonical_slug: Slug
    title: str = Field(min_length=3, max_length=600)
    publisher: Publisher
    source_id: Identifier
    document_family: DocumentFamily
    document_type: DocumentType = DocumentType.PDF
    jurisdiction: Jurisdiction | None = Jurisdiction.UK
    applicability: Applicability | None = Applicability.PUBLIC_PROCUREMENT
    year: int | None = Field(default=None, ge=1200, le=2200)
    language: str = Field(default="en", min_length=2, max_length=12)
    authoritative_url: AnyHttpUrl
    landing_url: AnyHttpUrl
    canonical_page_url: AnyHttpUrl | None = None
    first_seen_at: datetime
    first_seen_run_id: Identifier
    latest_seen_at: datetime
    latest_seen_run_id: Identifier
    latest_version_id: Identifier | None = None
    latest_sha256: Sha256 | None = None
    latest_download_url: AnyHttpUrl | None = None
    latest_http_status: int | None = Field(default=None, ge=200, le=599)
    latest_content_type: str | None = None
    latest_content_length: int | None = Field(default=None, ge=1)
    latest_etag: str | None = None
    latest_last_modified: str | None = None
    latest_downloaded_at: datetime | None = None
    latest_file_name_original: str | None = None
    latest_file_path_current: str | None = None
    latest_file_path_versioned: str | None = None
    version_count: int = Field(default=0, ge=0)
    status: LifecycleStatus = LifecycleStatus.ACTIVE
    supersedes_document_id: Identifier | None = None
    notes: str | None = Field(default=None, max_length=4000)

    @field_validator("first_seen_at", "latest_seen_at", "latest_downloaded_at")
    @classmethod
    def require_utc(cls, value: datetime | None) -> datetime | None:
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("Datetime must be timezone-aware.")
        return value.astimezone(UTC) if value else None

    @field_validator("authoritative_url", "landing_url", "canonical_page_url", "latest_download_url")
    @classmethod
    def require_official_host(cls, value: AnyHttpUrl | None) -> AnyHttpUrl | None:
        if value is None:
            return None
        host = urlparse(str(value)).hostname
        if not host or not (host == "gov.uk" or host.endswith(".gov.uk")):
            raise ValueError("URL host must be an approved government host.")
        return value

    @field_validator("latest_file_path_current", "latest_file_path_versioned")
    @classmethod
    def validate_relative_pdf_path(cls, value: str | None) -> str | None:
        if value is None:
            return None
        path = PurePosixPath(value.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts or not str(path).startswith("data/documents/"):
            raise ValueError("Document paths must be relative and start with data/documents/.")
        if path.suffix.lower() != ".pdf":
            raise ValueError("Document paths must point to a PDF file.")
        return path.as_posix()

    @model_validator(mode="after")
    def validate_lifecycle(self) -> Self:
        if self.latest_seen_at < self.first_seen_at:
            raise ValueError("latest_seen_at cannot be earlier than first_seen_at.")
        if self.status == LifecycleStatus.ACTIVE and self.version_count == 0 and self.latest_version_id is not None:
            raise ValueError("An active document with a version must have version_count >= 1.")
        return self


class Rejection(SchemaModel):
    rejection_id: Identifier
    run_id: Identifier
    source_id: Identifier | None = None
    url: AnyHttpUrl
    landing_url: AnyHttpUrl | None = None
    host: str = Field(min_length=1, max_length=255)
    reason_code: RejectionReason
    detail: str | None = Field(default=None, max_length=4000)
    robots_status: str | None = Field(default=None, pattern=r"^(allowed|disallowed|unreadable|unknown)$")
    occurred_at: datetime

    @field_validator("occurred_at")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must be timezone-aware.")
        return value.astimezone(UTC)
