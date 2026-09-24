# Enterprise Console Operations

**Status:** Service baseline  
**Applies to:** TODS Gateway v1.1.0

## Local start

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e "./SKBUK[test]"
uvicorn main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/`. API documentation is available at `/docs`; machine-readable service status is available at `/api/v1/status`.

## Release check

```bash
python -m pytest -q
```

Before any external service launch, verify:

1. TLS termination and approved host configuration;
2. authentication and scoped authorization (not implemented in this baseline);
3. rate and request-size controls at the edge;
4. durable audit and retention behavior (not implemented in this baseline);
5. current source/evidence lineage for every supported assurance outcome;
6. dependency, vulnerability, and secret scans;
7. backup, rollback, incident ownership, and monitoring;
8. legal, accessibility, privacy, and service-owner approval.

## Supported service claim

The current console is suitable for demonstration and controlled internal evaluation. It submits text to the executable SKBUK calibration route, displays actual response fields, creates a per-request correlation ID, and preserves the mandatory human-review status.

It is not yet suitable for unsupervised production assurance or a public launch because authentication, durable auditing, complete evidence verification, and direct specialist execution for all 34 MOUUK modules are not implemented.
