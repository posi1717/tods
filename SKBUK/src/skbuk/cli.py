from pathlib import Path
import json
import typer
import httpx
from skbuk.services.allowlist import approve
from skbuk.services.validator import validate_pdf
from skbuk.services.snapshot import lock_snapshot
from skbuk.utils.timestamps import utc_now, iso_z
from skbuk.settings import Settings
from skbuk.services.collection import collect as collect_documents
from skbuk.repositories.supabase_registry import SupabaseRegistry
from skbuk.services.provenance import ProvenanceWriter

app = typer.Typer(no_args_is_help=True)
source_app = typer.Typer(no_args_is_help=True)
snapshot_app = typer.Typer(no_args_is_help=True)
registry_app = typer.Typer(no_args_is_help=True)
app.add_typer(source_app, name="source")
app.add_typer(snapshot_app, name="snapshot")
app.add_typer(registry_app, name="registry")


def emit(payload: object, json_output: bool) -> None:
    if json_output:
        typer.echo(json.dumps(payload, default=str))
    else:
        typer.echo(payload if isinstance(payload, str) else json.dumps(payload, indent=2, default=str))


@source_app.command("validate")
def source_validate(url: str, dry_run: bool = True, json_output: bool = typer.Option(False, "--json")) -> None:
    del dry_run
    ok = approve(url)
    emit({"url": url, "allowed": ok, "reason": None if ok else "host_not_allowlisted"}, json_output)
    raise typer.Exit(0 if ok else 2)


@app.command("collect")
def collect(config: Path = typer.Option(..., "--config"), source: str | None = None, dry_run: bool = False, json_output: bool = typer.Option(False, "--json")) -> None:
    if source is not None:
        raise typer.BadParameter("source filtering is not yet supported; use an enabled source config")
    if not config.is_file():
        raise typer.BadParameter("config must be an existing file")
    settings = Settings()
    registry = None
    try:
        if settings.has_server_credentials and not dry_run:
            registry = SupabaseRegistry.from_settings(settings)
        result = collect_documents(
            config,
            Path(settings.skbuk_storage_root),
            settings.skbuk_user_agent,
            settings.skbuk_max_download_bytes,
            settings.skbuk_timeout_seconds,
            dry_run,
            provenance=ProvenanceWriter(registry) if registry else None,
        )
    finally:
        if registry:
            registry.client.close()
    emit(result.as_dict(), json_output)


@app.command("extract")
def extract(document_version: str = typer.Option(..., "--document-version"), dry_run: bool = False, json_output: bool = typer.Option(False, "--json")) -> None:
    emit({"status": "requires-local-version-path", "document_version": document_version, "dry_run": dry_run}, json_output)


@app.command("classify")
def classify(document_version: str = typer.Option(..., "--document-version"), dry_run: bool = False, json_output: bool = typer.Option(False, "--json")) -> None:
    emit({"status": "requires-registry-record", "document_version": document_version, "dry_run": dry_run}, json_output)


@app.command("report")
def report(run: str = typer.Option(..., "--run"), dry_run: bool = False, json_output: bool = typer.Option(False, "--json")) -> None:
    emit({"status": "report-command-ready", "run_id": run, "dry_run": dry_run}, json_output)


@snapshot_app.command("create")
def snapshot_create(tender: str = typer.Option(..., "--tender"), dry_run: bool = False, json_output: bool = typer.Option(False, "--json")) -> None:
    emit({"status": "open", "tender_id": tender, "dry_run": dry_run}, json_output)


@snapshot_app.command("lock")
def snapshot_lock(inspection_run: str = typer.Option(..., "--inspection-run"), version_id: list[str] = typer.Option([], "--version-id"), dry_run: bool = False, json_output: bool = typer.Option(False, "--json")) -> None:
    snapshot = lock_snapshot(inspection_run, "unknown", version_id, utc_now())
    emit({"status": "locked", "inspection_run_id": snapshot.inspection_run_id, "version_ids": snapshot.source_version_ids, "locked_at": iso_z(snapshot.locked_at), "dry_run": dry_run}, json_output)


@app.command("storage-verify")
def storage_verify(dry_run: bool = False, json_output: bool = typer.Option(False, "--json")) -> None:
    settings = Settings()
    if dry_run:
        emit({"status": "not_checked", "reason": "dry_run", "configured": settings.has_server_credentials}, json_output)
        return
    if not settings.has_server_credentials:
        emit({"status": "not_configured", "configured": False}, json_output)
        raise typer.Exit(2)
    registry = SupabaseRegistry.from_settings(settings)
    try:
        connected = registry.healthcheck()
    except httpx.HTTPError as exc:
        emit({"status": "unavailable", "configured": True, "reason": str(exc)}, json_output)
        raise typer.Exit(1) from exc
    finally:
        registry.client.close()
    emit({"status": "connected" if connected else "unauthorized_or_unavailable", "configured": True}, json_output)
    if not connected:
        raise typer.Exit(1)


@registry_app.command("export")
def registry_export(format: str = typer.Option(..., "--format"), dry_run: bool = False, json_output: bool = typer.Option(False, "--json")) -> None:
    if format not in {"csv", "json"}:
        raise typer.BadParameter("format must be csv or json")
    emit({"status": "registry-export-ready", "format": format, "dry_run": dry_run}, json_output)


if __name__ == "__main__":
    app()
