from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    supabase_url: str | None = None
    supabase_publishable_key: str | None = None
    supabase_service_role_key: str | None = None
    skbuk_storage_root: str = "./data"
    skbuk_user_agent: str = "SKBUK/0.1"
    skbuk_max_download_bytes: int = 150_000_000
    skbuk_timeout_seconds: float = 30.0

    @property
    def has_server_credentials(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_role_key)
