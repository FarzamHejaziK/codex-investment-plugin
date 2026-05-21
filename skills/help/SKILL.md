---
name: "help"
description: "Use when the user asks for help, orientation, troubleshooting, safety explanation, workflow guidance, or strategy-file explanation for the Codex Investment Assistant workspace."
---

# Help

Help the user understand and operate this investment workspace.

## Explain The Loop

- `config/workspace.json` stores non-secret workspace settings.
- `strategies/*.md` stores user-authored investment rules.
- `journal/YYYY-MM-DD.md` stores daily memos and execution records.
- `scripts/setup-workspace.py` creates/checks local workspace files.
- `scripts/alpaca-mcp-wrapper.sh` starts the Alpaca MCP server without storing secrets in the repo.

## Route Requests

- Setup/configuration: use the setup workflow.
- Daily portfolio check: use the daily workflow.
- New strategy: use the new-strategy workflow.
- Concepts, troubleshooting, docs, or safety: answer directly and reference local files.

## Rules

- Help does not place trades.
- Help does not write strategy files unless the user explicitly asks for an edit.
- If the user asks for a slash command, tell them this workspace uses natural language: "help me understand this investment workspace."
