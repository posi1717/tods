from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field, model_validator


class InspectionStatus(StrEnum):
    OPEN = "open"
    COMPLETED = "completed"
    LOCKED = "locked"


class InspectionRun(BaseModel):
    model_config = ConfigDict(extra="forbid")
    inspection_run_id: str
    tender_id: str
    status: InspectionStatus = InspectionStatus.OPEN
    locked_version_ids: list[str] = Field(default_factory=list)
    locked_at: datetime | None = None

    @model_validator(mode="after")
    def require_snapshot_when_locked(self):
        if self.status in {InspectionStatus.COMPLETED, InspectionStatus.LOCKED} and not self.locked_version_ids:
            raise ValueError("completed or locked inspections require exact version IDs")
        return self


class ComplianceCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    check_id: str
    inspection_run_id: str
    outcome: str
    evidence_excerpt_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_evidence_for_affirmative(self):
        if self.outcome.lower() in {"yes", "compliant", "affirmative", "pass"} and not self.evidence_excerpt_ids:
            raise ValueError("affirmative compliance checks require evidence excerpt IDs")
        return self
