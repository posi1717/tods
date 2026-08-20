# UK-KB-Collector — Codebase Overview & Target-Architecture Gap Analysis

**Date of analysis:** 20 Aug 2026 · **Mode:** Explore (inspection only, nothing modified)

---

## Answers to the 8 Questions

### 1. What files and folders currently exist?

Full tree (verified via recursive listing):

```
UK-KB-Collector/
├── .gitignore
├── .vscode/
│   ├── settings.json          # ⚠ contains macOS path /opt/homebrew/bin/python3 — broken on Windows
│   └── extensions.json
├── config.yaml                # version 1; sources, keywords, categories, compliance, limits
