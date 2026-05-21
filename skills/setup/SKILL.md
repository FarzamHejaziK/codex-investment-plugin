---
name: "setup"
description: "Use when the user asks to set up, configure, or initialize the Codex Investment Assistant workspace, Alpaca MCP, paper/live mode, execution mode, or local investment files."
---

# Setup

Set up this cloned repo as the user's Codex Investment Assistant workspace.

## Workflow

1. Run `python3 scripts/setup-workspace.py --json` from the repo root.
2. Tell the user where the workspace, config, strategies, and journal are.
3. Ask whether they want Alpaca **paper** or **live** mode.
4. Ask which execution mode they want:
   - `proposal-only` recommended: Codex writes memos and proposed orders; the user places orders manually.
   - `trading-with-confirmation`: Codex may place only the exact displayed order batch after exact confirmation.
5. Persist non-secret choices:

```bash
python3 scripts/setup-workspace.py --alpaca-account-mode <paper|live> --execution-mode <proposal-only|trading-with-confirmation>
```

6. Walk the user through Alpaca key generation:
   - Paper: `https://app.alpaca.markets/paper/dashboard/overview`
   - Live: `https://app.alpaca.markets/live/dashboard/overview`
7. Store keys outside the repo. On macOS, prefer Keychain:

```bash
read -s "k?Paste ALPACA_API_KEY: " && echo && \
  security add-generic-password -a "$USER" -s alpaca-api-key -w "$k" -U && unset k

read -s "s?Paste ALPACA_SECRET_KEY: " && echo && \
  security add-generic-password -a "$USER" -s alpaca-secret-key -w "$s" -U && unset s
```

8. Add or update the Alpaca MCP server in Codex using `scripts/alpaca-mcp-wrapper.sh`.
9. Verify the Alpaca connection with read-only account data only.
10. Explain how to activate a strategy: copy or edit a non-example file in `strategies/`, set `status: active`, and review `capital_monthly_usd`.

## Rules

- Never put API keys in `config/`, strategies, journal, docs, or chat.
- Setup never places trades.
- Default to proposal-only if the user is unsure.
- If the user asks for a slash command, tell them this workspace uses natural language: "set up my investment workspace."
