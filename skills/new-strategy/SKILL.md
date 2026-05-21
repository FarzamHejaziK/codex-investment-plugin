---
name: "new-strategy"
description: "Use when the user wants to create, draft, design, or generate a new investment strategy file for the Codex Investment Assistant workspace."
---

# New Strategy

Create a new paused strategy file under `strategies/`.

## Workflow

1. Run `python3 scripts/setup-workspace.py --json`.
2. Ask one question at a time:
   - strategy name and filename
   - goal
   - account mode: paper or live
   - monthly or total budget
   - allowed tickers
   - buy rules
   - sell rules, if any
   - sizing rules
   - risk limits
   - review cadence
3. Draft the strategy and show a concise summary before writing.
4. Write `strategies/<name>.md` only after user approval.
5. Default frontmatter must include:

```yaml
---
name: <name>
status: paused
account: alpaca-paper
capital_monthly_usd: 0
version: 1
last_updated: YYYY-MM-DD
---
```

6. Tell the user how to activate it: edit the file, review every rule, then set `status: active`.

## Rules

- Never create an active strategy by surprise.
- Never place trades from this skill.
- Keep the file human-readable markdown.
- If the user asks for a slash command, tell them this workspace uses natural language: "create a new investment strategy."
