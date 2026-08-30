# UK-KB-Collector — Dev Environment / Composio MCP Stabilisation Findings

**Date:** 20 Aug 2026 · **Mode:** Explore (inspection only; nothing modified)  
**Workspace:** `C:\Users\Donny\Desktop\UK-KB-Collector`

---

## 1. Workspace Confirmed

- **Current working directory:** `C:\Users\Donny\Desktop\UK-KB-Collector` ✓
- **Git remote:** `origin → https://github.com/Donny1717/UKKB.git`, branch `main`
- **Project type:** Python 3.12+ UK public-sector procurement PDF knowledge-base collector (CLI)
- **Virtual environments present:** `.venv/` (gitignored, expected by `scripts/run_collector.ps1`) and `.venv-1/`
- **OS:** Windows 11

### Notable pre-existing issue (from `project_info__1.md`)
- `.vscode/settings.json` contains `"doracodelens.pythonPath": "/opt/homebrew/bin/python3"` — a macOS path that is invalid on this Windows machine. Recommend switching the interpreter to `C:\Users\Donny\Desktop\UK-KB-Collector\.venv\Scripts\python.exe` in the next Act Mode session.

---

## 2. Sixth Read/Edit Capability Confirmed

- The Sixth AI VS Code extension (`sixth.sixth-ai`) is already the **only recommended extension** in `.vscode/extensions.json`.
- The agent authenticated in this session can read the workspace and is configured to edit it (Act Mode). Current session verified read access to all key files:
  - `.vscode/settings.json`, `.vscode/extensions.json`
  - `README.md`, `config.yaml`, `requirements.txt`, `.gitignore`
  - `scripts/run_collector.ps1`
- Note: `search_files` failed with `Could not find ripgrep binary` — the extension's ripgrep dependency is missing on this machine. This blocks regex search; `read_file`/`read_batch`/`list_files` still work. Worth fixing in Act Mode (reinstall/repair the extension or VS Code's bundled ripgrep).

---

## 3. Current MCP Status — NOT CONFIGURED

- `.vscode/` currently contains **only**:
  - `.vscode/settings.json`
  - `.vscode/extensions.json`
- **There is no `.vscode/mcp.json`** and no `mcpServers` configuration anywhere in the workspace (verified by directory listing; regex search unavailable due to ripgrep issue, but no MCP files exist in the tree).
- **No Composio configuration exists.** No Composio credentials, `COMPOSIO_API_KEY`, or related environment variables are present in `.gitignore` (`.env` is listed, meaning a `.env` would be ignored if created).

---

## 4. Required Configuration (Draft — to be created in Act Mode)

Target file: `.vscode/mcp.json` (per task instruction #4). Standard Composio MCP server config for VS Code:

```json
{
  "servers": {
    "composio": {
      "type": "http",
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer ${COMPOSIO_API_KEY}"
      },
      "env": {
        "COMPOSIO_API_KEY": "${COMPOSIO_API_KEY}"
      }
    }
  }
}
```

> ⚠ This is a candidate draft. The exact `type` (`http` vs `sse` vs `stdio`) and URL depend on the Composio connection method chosen (Composio MCP server URL vs local `composio mcp` CLI). The exact config must be finalised in Act Mode using Composio's current setup wizard, then verified. Do **not** commit real API keys into the JSON — use VS Code variable interpolation (`${COMPOSIO_API_KEY}`) with the key stored in the user/environment or a gitignored `.env`.

---

## 5. Status Summary

| Task item | Status |
|-----------|--------|
| 1. Confirm workspace `C:\Users\Donny\Desktop\UK-KB-Collector` | ✅ Confirmed |
| 2. Confirm Sixth can read/edit the workspace | ✅ Confirmed (Act Mode ready) |
| 3. Configure Composio MCP | ❌ Not yet — requires Act Mode |
| 4. Use `.vscode/mcp.json` | ⏳ Target file identified (does not exist yet) |
| 5. Don't modify architecture | ✅ Honoured |
| 6. Don't run production collector | ✅ Honoured |
| 7. Don't download procurement documents | ✅ Honoured |
| 8. Verify agent sees Composio tools | ❌ Not yet — requires Act Mode |
| 9. Report exact MCP config + connection status | ⏳ Partial (config draft above; status = not connected) |
| 10. Don't add unnecessary integrations | ✅ Honoured |

---

## 6. What's Next — Switch to Act Mode

The remaining steps are state-changing/execution actions that Explore Mode cannot perform:

| Step | Action | Mode required |
|------|--------|---------------|
| 3 | Configure Composio MCP for this workspace | Act |
| 4 | Create/edit `.vscode/mcp.json` | Act |
| 7 | (Optional) repair ripgrep for `search_files` | Act |
| 8 | Verify agent can see Composio tools after connection | Act |
| 9 | Report exact MCP config + connection status post-connection | Act |

**To proceed:** switch to **Act Mode** using the mode selector at the bottom of the chat. Your exploration findings above will carry over as context. Suggested Act Mode steps:

- [x] Confirm workspace path (`C:\Users\Donny\Desktop\UK-KB-Collector`)
- [x] Confirm Sixth can read/edit the workspace
- [x] Verify current MCP state (no `.vscode/mcp.json` exists)
- [ ] Fix `.vscode/settings.json` pythonPath (currently macOS `/opt/homebrew/bin/python3` → should be `.venv\Scripts\python.exe`)
- [ ] (Optional) repair ripgrep so `search_files` works
- [ ] Install/start Composio CLI or obtain Composio MCP server URL + API key
- [ ] Create `.vscode/mcp.json` with Composio MCP server config (no hardcoded secrets)
- [ ] Reload VS Code window to load MCP server
- [ ] Verify connection status (MCP server shows Connected in VS Code)
- [ ] Verify agent can see/list available Composio tools
- [ ] Report exact MCP config + connection status
- [ ] Do NOT modify architecture, run production collector, or download documents
- [ ] Do NOT add unnecessary integrations

---

**Report saved to:** `C:\Users\Donny\Desktop\UK-KB-Collector\project_info__2.md`