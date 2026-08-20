# UK Public Sector Procurement PDF Collector

A Windows-first, Python 3.12+ knowledge-base collector for official UK public procurement PDFs. It discovers PDF links from configured official landing pages, validates and hashes files, classifies them into a controlled folder structure, preserves previous versions, and writes a CSV/JSON registry plus per-run logs and Markdown reports.

## Scope and compliance

This collector is designed for public, official sources only. It allowlists `gov.uk`, `*.gov.uk`, `legislation.gov.uk`, and `*.legislation.gov.uk` by default. It refuses a source when `robots.txt` cannot be read or says the collector is disallowed.

The software does not attempt to bypass authentication, paywalls, CAPTCHAs, anti-bot systems, or access controls. It does not automatically delete prior documents. It stores source URLs, landing pages, timestamps, hashes, ETags and HTTP Last-Modified values in the registry.

This is a knowledge-base collector, not legal advice. Government guidance and legislation can be amended or replaced. Always verify the current version on the official source before using a document operationally.

## Architecture

`discover -> robots/rate-limit gate -> PDF download -> PDF/magic-byte validation -> SHA-256 -> metadata/text probe -> relevance classification -> version/archive -> registry -> report`

The package is organised into three layers:

- `core/`: orchestration contracts and the canonical MOUUK module registry;
- `workers/`: 26 independent knowledge and reasoning API plugins using a shared contract;
- `intelligence/`: authority, temporal, relationship and evidence engines.

Collection and reasoning are deliberately separated. The existing discovery and
collector pipeline is the ingestion service: it finds, validates, versions and registers
official documents. The 26 plugins do not crawl the web. They receive selected registry
evidence through `ReasoningRequest`, apply their own specialist rules and taxonomy, and
return a standard `ReasoningResponse` containing reasoning steps, citations, confidence
and a review flag.

Stable module identities are defined in `uk_kb_collector/modules.yaml`. Codes are never
reused after publication. Every entry from MOUUK-0001 through MOUUK-0026 is independently
loadable and owns its manifest, sources, rules, taxonomy and reasoning worker. TOMs retains
its semantic relationship to Social Value without sharing its worker implementation.

Key modules:

- `discover.py`: fetches configured official collection/landing pages and finds PDF links.
- `http.py`: polite HTTP client with per-domain throttling, retries and robots handling.
- `pdf.py`: streaming-safe validation and bounded PDF metadata/text extraction.
- `categorize.py`: deterministic title/URL/content-based categorisation and relevance tags.
- `registry.py`: CSV/JSON registry indexed by URL, hash and filename.
- `collector.py`: versioning, archive and storage orchestration.
- `report.py`: per-run Markdown report.
- `main.py`: CLI entry point.

## Project structure

```text
uk-kb-public-sector-collector/
├── config.yaml
├── requirements.txt
├── README.md
├── .gitignore
├── scripts/
│   └── run_collector.ps1
├── uk_kb_collector/
│   ├── __init__.py
│   ├── categorize.py
│   ├── collector.py
│   ├── config.py
│   ├── discover.py
│   ├── http.py
│   ├── main.py
│   ├── models.py
│   ├── pdf.py
│   ├── registry.py
│   ├── report.py
│   └── utils.py
└── tests/
    └── test_core.py
```

The collector creates this runtime tree under `~/Desktop/UK-KB-PUBLIC Sector`:

```text
00_Inbox/
01_Legislation/
  Procurement_Act_2023/
  Procurement_Regulations_2024/
  Legacy_Regulations/
  Other_Relevant_Legislation/
02_Statutory_Guidance/
03_Procurement_Policy_Notes/
04_NPPS_and_Government_Policy/
05_Cabinet_Office_Guidance/
  Plan/
  Define/
  Procure/
  Manage/
06_Frameworks_Standards_Playbooks/
07_Templates_and_Model_Documents/
08_Archive/
09_Logs/
10_Metadata/
  document_registry.csv
  document_registry.json
```

## Official seed sources

The default configuration includes:

- Procurement Act 2023 guidance collection.
- Procurement Policy Notes collection.
- Public procurement policy.
- Transforming Public Procurement collection.
- Procurement Act 2023.
- Procurement Regulations 2024.
- Public Contracts Regulations 2015.
- Utilities Contracts Regulations 2016.
- Concession Contracts Regulations 2016.
- Defence and Security Public Contracts Regulations 2011.
- Public Services (Social Value) Act 2012.

The GOV.UK Procurement Act guidance collection is organised into Plan, Define, Procure and Manage phases. The official page was updated during 2026, including changes to the guidance set. The PPN collection was also updated in June 2026. See the official source pages when reviewing current material.

## Installation on Windows

Open PowerShell in this project directory.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run unit tests:

```powershell
python -m pytest -q
```

## First run: dry-run

Dry-run is enabled by default in `config.yaml`. It temporarily downloads PDFs for
validation and classification, then deletes those temporary copies. It does not retain
collected PDFs or add new document records, but it does create runtime directories,
logs, reports and registry files.

```powershell
python -m uk_kb_collector.main --dry-run
```

Review:

```text
Desktop\UK-KB-PUBLIC Sector\09_Logs\run_*.log
Desktop\UK-KB-PUBLIC Sector\09_Logs\report_*.md
```

## Production mode

After reviewing the dry-run output:

```powershell
python -m uk_kb_collector.main --production
```

Or set `dry_run: false` in `config.yaml` and run without an override.

## Registry and versioning behaviour

Each source PDF URL has a stable URL-derived identity for its first active version. When a URL returns the same hash, the run is recorded as checked and the file is skipped. When a URL returns a different hash, the previous file is moved to `08_Archive/` and the newly downloaded copy receives the next `vX` filename plus an immutable version record id. Old registry rows remain present and are marked `superseded`.

The collector does not claim a publication date unless a source parser supplies one. In this baseline implementation, unknown publication dates are written as `undated`, while HTTP `Last-Modified` is retained separately in metadata.

## Windows Task Scheduler — every 2 hours

1. Create the project at a permanent location, for example `C:\Users\<you>\Documents\uk-kb-public-sector-collector`.
2. Confirm the virtual environment exists at `.venv`.
3. Test production mode manually once.
4. Open **Task Scheduler** -> **Create Task...**.
5. **General** tab:
   - Name: `UK Procurement KB Collector`
   - Select **Run whether user is logged on or not**.
   - Select **Run with highest privileges** only if your corporate policy requires it; the collector itself normally does not need elevation.
6. **Triggers** -> **New...**:
   - Begin the task: `On a schedule`.
   - Daily.
   - Set a convenient start time.
   - Check **Repeat task every: 2 hours** for a duration of **Indefinitely**.
   - Ensure the trigger is enabled.
7. **Actions** -> **New...**:
   - Action: `Start a program`.
   - Program/script: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
   - Add arguments:
     `-NoProfile -ExecutionPolicy Bypass -File "C:\PATH\TO\uk-kb-public-sector-collector\scripts\run_collector.ps1" -Production`
   - Start in:
     `C:\PATH\TO\uk-kb-public-sector-collector`
8. **Conditions**: optionally uncheck the AC power restriction if you need the task to run on battery.
9. **Settings**:
   - Allow task to be run on demand.
   - If the task fails, restart it after 5 minutes; choose a small retry count if required.
   - Avoid overlapping runs by enabling **Do not start a new instance** if one is already running.
10. Save the task. Windows will request the account password for the selected non-interactive logon mode.

The PowerShell launcher changes directory to the project first, so the virtual environment and relative paths work correctly. Python stdout/stderr are also mirrored into `09_Logs/run_*.log` by the application. Task Scheduler history can be enabled for execution diagnostics.

### Alternative: run the Python interpreter directly

You can set **Program/script** to:

```text
C:\PATH\TO\uk-kb-public-sector-collector\.venv\Scripts\python.exe
```

Arguments:

```text
-m uk_kb_collector.main --production
```

Start in:

```text
C:\PATH\TO\uk-kb-public-sector-collector
```

This is the simplest Task Scheduler configuration because it does not rely on shell activation.

## macOS launchd

Use a user LaunchAgent at `~/Library/LaunchAgents/com.local.uk-procurement-kb.plist` and invoke the virtualenv Python directly.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.local.uk-procurement-kb</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/YOU/PATH/uk-kb-public-sector-collector/.venv/bin/python</string>
    <string>-m</string><string>uk_kb_collector.main</string><string>--production</string>
  </array>
  <key>WorkingDirectory</key><string>/Users/YOU/PATH/uk-kb-public-sector-collector</string>
  <key>StartInterval</key><integer>7200</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>/Users/YOU/PATH/uk-kb-public-sector-collector/09_stdout.log</string>
  <key>StandardErrorPath</key><string>/Users/YOU/PATH/uk-kb-public-sector-collector/09_stderr.log</string>
</dict>
</plist>
```

Load it with:

```bash
launchctl load ~/Library/LaunchAgents/com.local.uk-procurement-kb.plist
```

## Linux cron

Edit the user's crontab:

```bash
crontab -e
```

Every two hours:

```cron
0 */2 * * * cd /path/to/uk-kb-public-sector-collector && /path/to/uk-kb-public-sector-collector/.venv/bin/python -m uk_kb_collector.main --production >> /path/to/uk-kb-public-sector-collector/cron_stdout.log 2>> /path/to/uk-kb-public-sector-collector/cron_stderr.log
```

For a workstation daemon with better restart semantics, use a `systemd` user timer instead of cron.

## Configuration

Edit `config.yaml` rather than Python code to change:

- source URLs and category hints;
- keywords and exclusions;
- allowed domains;
- destination directory;
- polling interval metadata;
- request timeout/retry/backoff controls;
- PDF size limits;
- dry-run/production default.

The collector intentionally does not use search-engine scraping as its source of truth. External sources can be used manually to discover an official landing page, after which that official URL can be added to `sources:`.

## Operational notes

- `robots.txt` is checked before each source/download URL.
- Requests to the same domain are throttled to at least the configured delay.
- Downloads use timeouts, bounded retries and exponential backoff.
- PDF streaming enforces a maximum file size.
- PDF magic bytes and Content-Type are checked before storage.
- The code never deletes an archived document automatically.
- A file is never replaced in-place when its hash changes.
- Classification is deterministic and conservative; uncertain documents go to `00_Inbox` with `NEEDS_REVIEW`.
- The collector does not summarise or alter legal content during collection.
#   U K K B  
 