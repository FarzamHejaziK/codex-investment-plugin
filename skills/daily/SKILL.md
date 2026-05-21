---
name: "daily"
description: "Use when the user asks to run the daily investment checkpoint, read active strategies, pull Alpaca portfolio data, write the daily memo, propose orders, or execute a confirmed trade batch."
---

# Daily

Run the daily investment checkpoint from this workspace.

## Workflow

1. Run `python3 scripts/setup-workspace.py --json` and read `config/workspace.json`.
2. Read every non-example `strategies/*.md` file with `status: active`.
3. If there are no active strategies, stop and tell the user how to activate or create one.
4. Confirm Alpaca MCP is available before making portfolio or market claims.
5. Pull read-only account, positions, buying power, open orders, recent activity, and needed market data.
6. Evaluate each active strategy exactly as written:
   - allowed universe
   - buy/sell rules
   - sizing rules
   - budget limits
   - risk controls
7. Write `journal/YYYY-MM-DD.md` with:
   - account snapshot
   - strategy-by-strategy analysis
   - proposed orders
   - skipped ideas and reasons
   - risk notes
   - execution section, if any
8. Show the memo summary and proposed order table in chat.

## Trading

Proposal-only is the default. In proposal-only mode, never submit orders.

If `config/workspace.json` says `trading-with-confirmation`:

1. Show the exact order batch.
2. Ask the user to type exactly:

```text
EXECUTE <N> ORDERS
```

3. Only submit the exact displayed orders if the phrase matches the batch count.
4. Record Alpaca order IDs in the journal.

## Rules

- Do not invent quotes, positions, balances, or news.
- Do not trade outside strategy universes.
- Do not submit undisplayed or modified orders.
- Do not auto-edit operational strategy sections.
- If the user asks for a slash command, tell them this workspace uses natural language: "run my daily investment checkpoint."
