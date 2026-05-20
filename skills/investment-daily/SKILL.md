---
name: "investment-daily"
description: "Use when the user asks to run the daily investment checkpoint, read active strategies, pull Alpaca portfolio data, write the daily memo, propose orders, or execute a confirmed trade batch."
---

# Investment Daily

This skill is the daily-checkpoint surface for the Codex Investment Assistant plugin.

Follow the canonical daily procedure in `../../commands/investment-daily.md`.

Hard safety rules:

1. Run `python3 scripts/workspace-bootstrap.py --json` first and use the returned workspace.
2. Proposal-only is the default and must never place orders.
3. Trading is allowed only when workspace config says `trading-with-confirmation` and the user types the exact displayed `EXECUTE <N> ORDERS` phrase for the exact batch.
4. Do not invent portfolio, quote, order, or market data. If Alpaca MCP is missing, stop and say so.

If the user expected a slash command, tell them the command is `/investment-daily`.
