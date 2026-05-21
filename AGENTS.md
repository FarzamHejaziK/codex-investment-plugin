# AGENTS.md

This is a **Codex Investment Assistant workspace** built around Codex plus the Alpaca MCP. The cloned repo is the workspace: strategies, journal entries, local config, docs, scripts, and skills all live here.

## How To Behave

When the user asks for investment assistant work, route to the local skill files:

- Setup: read `skills/setup/SKILL.md`.
- Daily checkpoint: read `skills/daily/SKILL.md`.
- New strategy: read `skills/new-strategy/SKILL.md`.
- Help and troubleshooting: read `skills/help/SKILL.md`.

The user does not need plugin install commands or slash commands. Natural language is the intended interface.

## Hard Rules

1. **Default to proposal-only.** Do not place trades unless `config/workspace.json` says `trading-with-confirmation` and the user has typed the exact confirmation phrase for the displayed order batch.
2. **Use read-only Alpaca calls for analysis.** Account, positions, activity, quotes, bars, and open orders are allowed. Order-placement tools are allowed only inside the confirmed execution section of the daily workflow.
3. **Do not auto-edit operational strategy sections.** Frontmatter, Watchlist/Universe, Buy strategy, Sizing rules, Risk rules, and Profile are the user's rules. Ask before changing them.
4. **Never store API keys in this repo.** Not in `config/`, `.env`, strategy files, journal files, docs, or chat. Keys live in OS keychain or user-managed environment.
5. **Do not fabricate data.** If Alpaca MCP is unavailable or market data is stale, say so.
6. **This is not financial advice.** The user's strategy files are the authority.

## Workspace Map

- `config/workspace.example.json` - tracked example config.
- `config/workspace.json` - generated local config, ignored by git.
- `strategies/` - user-authored investment rules. Example files ship paused.
- `journal/` - daily memos and optional execution records.
- `skills/` - the four workflow guides Codex should use.
- `scripts/setup-workspace.py` - idempotently creates/checks local workspace files.
- `scripts/alpaca-mcp-wrapper.sh` - starts the Alpaca MCP server from external secrets.
- `scripts/validate-workspace.py` - checks repo health before publishing.
- `docs/` - user docs.

Always read relevant local files before answering questions about them.
