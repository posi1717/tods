from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class DocumentVersion(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    version_id: str
    document_id: str
    run_id: str
    download_url: HttpUrl
    http_status: int = Field(ge=200, le=599)
    content_type: str
    content_length: int | None = Field(default=None, ge=1)
    etag: str | None = None
    last_modified: str | None = None
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    file_name_original: str | None = None
    storage_bucket: str = "tod-official"
    storage_path: str
    discovered_at: datetime
    downloaded_at: datetime
    is_binary_changed: bool

    @field_validator("storage_bucket")
    @classmethod
    def official_versions_use_official_bucket(cls, value: str) -> str:
        if value != "tod-official":
            raise ValueError("official source versions must use tod-official")
        return value
