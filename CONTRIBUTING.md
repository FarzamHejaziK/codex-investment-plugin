# Contributing

This repo is a Codex plugin adapted from the Claude Investment Assistant template. Contributions should improve the plugin, prompts, scripts, docs, examples, or safety model.

## Helpful contributions

- Bug fixes in `commands/*.md`
- Workspace bootstrap improvements
- Alpaca setup and MCP troubleshooting improvements
- Documentation fixes
- Safer trading-with-confirmation guardrails
- Improvements to example strategy clarity

## Out of scope

- Financial advice
- New opinionated investment strategies as defaults
- Autonomous trading without per-run user confirmation
- Secrets, account data, or personal journal examples

## Development rules

1. Test Alpaca changes with paper trading first.
2. Never commit API keys, account numbers, private strategy files, or journal entries.
3. Keep example strategies `status: paused`.
4. Update docs when behavior changes.
5. Treat live trading paths as high risk: every order path must be explicit, confirmed, and auditable.

## Validation

Run:

```bash
python3 scripts/validate-plugin.py
```

Also run the workspace bootstrap manually:

```bash
python3 scripts/workspace-bootstrap.py --json
```

## License

By contributing, you agree your contributions are licensed under the MIT license.
