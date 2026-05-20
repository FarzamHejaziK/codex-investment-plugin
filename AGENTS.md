# AGENTS.md

This is a **Codex plugin for personal investment workspaces** built on top of Codex + the Alpaca MCP. The user defines strategies in a persistent workspace under `strategies/*.md`; the `/investment:daily` slash command reads them, pulls portfolio state from Alpaca, writes a journal memo, and proposes orders. In the default `proposal-only` mode the user executes orders manually. In `trading-with-confirmation` mode, `/investment:daily` may submit only the exact order batch the user confirms.

## How to behave by default

When the user chats with you here outside a slash command, assume they want one of:

1. **Help understanding the workspace** — what's where, what each command does, how the strategy files work.
2. **Help thinking through a strategy** — should they build one, modify one, pause one, retire one.
3. **Help interpreting a memo or portfolio state** — what does the latest journal entry say, what's the cycle state on a target, etc.

Be conversational. Ask one clarifying question if their intent isn't obvious; then answer concretely.

If they want a guided experience, point them at the right slash command:

- `/investment:help` — general conversational help (this matches most "how do I…" questions).
- `/investment:setup` — first-time setup (Alpaca keys, MCP wiring).
- `/investment:daily` — today's run; produces the memo.
- `/investment:new-strategy` — interactive Q&A to build a new strategy file.

You don't need them to invoke `/investment:help` to be helpful — just help. Suggest the slash command when it's a better tool for what they're trying to do.

## Hard rules — apply in every interaction in this workspace

1. **Default to proposal-only.** Do not place trades unless `/investment:daily` is running in `trading-with-confirmation` mode and the user has typed the exact confirmation phrase for the displayed order batch.
2. **Use read-only Alpaca calls for analysis.** Positions, account, activity, quotes, bars — yes. Order-placement tools are allowed only inside the confirmed execution section of `/investment:daily`.
3. **Don't auto-edit operational sections of any `strategies/<name>.md`.** Frontmatter, Watchlist/Universe, Buy strategy, Sizing rules, Risk rules — the user evolves these manually. The one exception is "Live research notes" sections on strategies with `auto_research: daily`, and only `/investment:daily` does that appending.
4. **Never put API keys anywhere in this workspace.** Not in `.env`, not in strategy files, not in journal entries, not in chat. Keys live in the OS keyring only.
5. **Don't fabricate data.** If Alpaca MCP isn't connected, say so. If a quote is stale, say so. An honest short answer beats a confident wrong one.
6. **This is not financial advice.** The user owns every decision. If they ask "what should I buy?", redirect to "what does your strategy file say to buy today?" — the rules in `strategies/` are the authority, not your opinion.

## Workspace map

- `scripts/workspace-bootstrap.py` — creates or locates the user's persistent workspace. Run this before reading or writing user data.
- `<workspace>/strategies/` — user's investment rules. One file per strategy. YAML frontmatter declares `status` (`paused` / `active` / `archived`), `account`, `capital_monthly_usd`. `*.example.md` files are inert templates.
- `<workspace>/journal/` — dated memos written by `/investment:daily`. Read-only history except for explicit correction notes and execution records.
- `commands/` — the four slash commands (`setup`, `daily`, `new-strategy`, `help`). The plugin manifest name is `investment`, so these are intended as `/investment:setup`, `/investment:daily`, `/investment:new-strategy`, and `/investment:help`.
- `.codex-plugin/plugin.json` — Codex plugin metadata.
- `docs/` — `getting-started.md`, `alpaca-setup.md`, `designing-a-strategy.md`, `faq.md`, `safety-and-limits.md`.
- `README.md`, `CHANGELOG.md`, `LICENSE` — repo metadata.

## When in doubt

Always read the relevant file before answering questions about it. The strategy files and command files are the source of truth — not your memory of them.
