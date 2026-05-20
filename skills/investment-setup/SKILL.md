---
name: "investment-setup"
description: "Use when the user asks to set up, install, configure, or initialize the Codex Investment Assistant, Alpaca MCP, paper/live mode, execution mode, or the investment workspace."
---

# Investment Setup

This skill is the setup surface for the Codex Investment Assistant plugin.

Follow the canonical setup procedure in `../../commands/investment-setup.md`.

Before asking setup questions:

1. Run `python3 scripts/workspace-bootstrap.py --json` from the installed plugin root when possible.
2. Treat the returned `workspace_path` as the user's persistent investment workspace.
3. Never store Alpaca API keys in strategy files, journal files, docs, or chat.
4. Default execution mode to `proposal-only` unless the user explicitly chooses `trading-with-confirmation`.

If the user expected a slash command, tell them the command is `/investment-setup`.
