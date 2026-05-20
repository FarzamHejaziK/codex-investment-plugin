# Workspace bootstrap

The plugin code and user data are separate.

The installed plugin repo contains prompts, scripts, examples, and docs. Your personal strategies and journal entries live in a persistent workspace.

## Resolution order

`scripts/workspace-bootstrap.py` chooses the workspace in this order:

1. `CODEX_INVESTMENT_WORKSPACE`, if set
2. Current directory, if it contains `.investment-assistant-workspace.json`
3. `~/.codex-investment-plugin/config.json`, if it has a valid `workspace_path`
4. Default path:

   ```text
   ~/Documents/codex-investment-plugin-workspace
   ```

## What gets created

On first run, the script creates:

```text
<workspace>/
├── .investment-assistant-workspace.json
├── README.md
├── strategies/
│   ├── dip-buying.example.md
│   ├── ai-value-chain.example.md
│   └── active-trading.example.md
└── journal/
    └── .gitkeep
```

It also writes:

```text
~/.codex-investment-plugin/config.json
```

## Inspect the workspace

From the plugin repo:

```bash
python3 scripts/workspace-bootstrap.py --json
```

Example output:

```json
{
  "workspace_path": "/Users/you/Documents/codex-investment-plugin-workspace",
  "execution_mode": "proposal-only",
  "config_path": "/Users/you/.codex-investment-plugin/config.json"
}
```

## Override the workspace

```bash
export CODEX_INVESTMENT_WORKSPACE=/path/to/my-workspace
python3 scripts/workspace-bootstrap.py
```

The script creates the folder if needed and records it in config.

## Execution mode

Set proposal-only:

```bash
python3 scripts/workspace-bootstrap.py --execution-mode proposal-only
```

Set trading-with-confirmation:

```bash
python3 scripts/workspace-bootstrap.py --execution-mode trading-with-confirmation
```

The mode affects `/investment-daily`; setup, help, and strategy-builder commands never place trades.

## Privacy

Your workspace may contain strategy budgets, portfolio snapshots, proposed trades, and Alpaca order IDs. Keep it private unless you intentionally want to share that data.
