param(
  [switch]$Production
)
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot\..
if (-not (Test-Path .\.venv\Scripts\python.exe)) {
  Write-Error 'Virtual environment not found. Run: py -3.12 -m venv .venv'
}
if ($Production) {
  & .\.venv\Scripts\python.exe -m uk_kb_collector.main --production
} else {
  & .\.venv\Scripts\python.exe -m uk_kb_collector.main --dry-run
}
exit $LASTEXITCODE
