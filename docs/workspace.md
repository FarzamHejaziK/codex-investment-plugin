# Workspace

The cloned repo is the workspace. User data and workflow instructions live together so the setup is easy to inspect.

## Important Folders

```text
config/      local non-secret settings
strategies/  strategy examples and active strategy files
journal/     dated daily memos
skills/      Codex workflow instructions
scripts/     deterministic setup, MCP wrapper, validation
docs/        reference docs
```

## Local Config

`config/workspace.example.json` is tracked. `config/workspace.json` is generated and ignored by git.

Example:

```json
{
  "schema_version": 1,
  "workspace_type": "codex-investment-workspace",
  "execution_mode": "proposal-only",
  "alpaca_account_mode": "paper",
  "created_at": "2026-05-21T12:00:00+00:00"
}
```

This file must never contain API keys.

## Check Or Create Local Files

```bash
python3 scripts/setup-workspace.py --json
```

Set modes:

```bash
python3 scripts/setup-workspace.py --alpaca-account-mode paper --execution-mode proposal-only
python3 scripts/setup-workspace.py --alpaca-account-mode live --execution-mode trading-with-confirmation
```

## Privacy

Journal entries and non-example strategies may contain budgets, positions, and trade history. Keep the repo private or adjust `.gitignore` if you do not want those files committed.
