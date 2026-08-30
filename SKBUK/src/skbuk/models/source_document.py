from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from skbuk.taxonomy.official import OfficialFamily


class SourceDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document_id: str = Field(min_length=3)
    canonical_slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: str = Field(min_length=3, max_length=600)
    publisher: str
    source_id: str
    document_family: OfficialFamily
    document_type: str = "pdf"
    jurisdiction: str = "UK"
    authoritative_url: HttpUrl
    landing_url: HttpUrl
    first_seen_at: datetime
    latest_seen_at: datetime
    status: str = "active"
