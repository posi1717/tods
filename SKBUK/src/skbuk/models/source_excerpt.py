from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class SourceExcerpt(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    excerpt_id: str
    document_version_id: str
    page_start: int = Field(ge=1)
    page_end: int = Field(ge=1)
    heading_path: list[str] = Field(default_factory=list)
    text: str = Field(min_length=1)
    text_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    extractor_name: str
    extractor_version: str
    confidence: float = Field(ge=0, le=1)
    created_at: datetime
