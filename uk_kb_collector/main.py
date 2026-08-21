from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from .config import load_config
from .collector import run_once
from .registry import Registry
from .report import write_report
from .skbuk import sync_records


def configure_logging(log_dir: Path) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    from datetime import datetime
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    log_path = log_dir / f"run_{stamp}.log"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return log_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Official UK public procurement PDF collector with SKBUK knowledge gateway")
    parser.add_argument("--config", type=Path, default=Path("config.yaml"))
    parser.add_argument("--dry-run", action="store_true", help="override config and do not write downloaded PDFs")
    parser.add_argument("--production", action="store_true", help="override config and enable downloads")
    args = parser.parse_args()

    cfg = load_config(args.config.resolve())
    if args.dry_run and args.production:
        parser.error("use only one of --dry-run or --production")
    if args.dry_run:
        cfg = cfg.__class__(**{**cfg.__dict__, "dry_run": True})
    elif args.production:
        cfg = cfg.__class__(**{**cfg.__dict__, "dry_run": False})

    dirs = cfg.destination
    log_path = configure_logging(dirs / "09_Logs")
    logger = logging.LoggerAdapter(logging.getLogger("uk_kb_collector"), {"run_log": str(log_path)})
    logger.info("Starting collector; destination=%s dry_run=%s", cfg.destination, cfg.dry_run)
    logger.info("Legal notice: %s", cfg.legal_notice)

    summary = run_once(cfg, logger)

    # SKBUK owns the raw PDF store and MOUUK delivery manifests. MOUUK modules
    # receive references only; this stage deliberately does not chunk, embed or summarise.
    reg = Registry(dirs / "10_Metadata" / "document_registry.csv", dirs / "10_Metadata" / "document_registry.json")
    reg.load()
    skbuk_summary = sync_records(dirs, list(reg.all()), dry_run=cfg.dry_run)
    summary["skbuk"] = skbuk_summary
    logger.info("SKBUK sync: %s", json.dumps(skbuk_summary, ensure_ascii=False))

    report = write_report(dirs / "09_Logs", summary, cfg.dry_run)
    logger.info("Finished. report=%s summary=%s", report, json.dumps(summary, ensure_ascii=False))
    return 0 if not summary["failed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
