# Codex Investment Assistant Public Plugin Plan

## Current Implementation State

- Local repo path: `/Users/ferzamh/code-git-local/codex-investment-plugin`
- Source baseline: `FarzamHejaziK/claude-investment-assistant` `main` at commit `9607f6b52214f20e340c1c27491766b78b7acc78`
- Local remote:
  - `upstream` points at `https://github.com/FarzamHejaziK/claude-investment-assistant.git`
  - upstream push URL is disabled locally to avoid accidentally pushing Codex changes back to the Claude repo
- Added Codex plugin manifest: `.codex-plugin/plugin.json`
- Added Codex commands in `commands/investment/`
- Added workspace bootstrap, Alpaca wrapper, and validation scripts in `scripts/`
- Added Codex docs for workspace bootstrap and trading mode
- Removed the Claude runtime command/config directory from the Codex plugin
- This document is `.docs/plan.md`.

## Implementation Status

Implemented in this repo:

- Phase 1: upstream parity baseline and source attribution
- Phase 2: Codex command conversion
- Phase 3: workspace bootstrap
- Phase 4: Alpaca setup for Codex
- Phase 5: optional trading-with-confirmation mode
- Phase 6: documentation conversion
- Phase 7: validation script and dry-run bootstrap testing path

Remaining release operation:

- Phase 8: tag a release after final manual review and any marketplace/install workflow checks.

## Product Goal

Create a public Codex plugin that mirrors `FarzamHejaziK/claude-investment-assistant` as closely as possible, with only these intentional changes:

1. Replace Claude-specific packaging, commands, documentation, and setup wording with Codex equivalents.
2. Preserve the strategy-file workflow, examples, setup wizard, help command, new-strategy builder, daily memo format, journal behavior, and safety explanations unless Codex requires wording changes.
3. Add optional trading mode: when the user explicitly chooses trading and confirms the exact order batch, the plugin can place Alpaca orders directly.
4. Add workspace bootstrap behavior: when the plugin starts or a command runs and no workspace path is configured, create or locate a persistent user workspace and read/write strategy and journal files there.

The default behavior should remain proposal-only. Trading must be opt-in, explicit, auditable, and reversible only by the user's brokerage actions.

## Public Repo Strategy

Recommended approach: create a new public GitHub repo named `FarzamHejaziK/codex-investment-plugin`, not a GitHub fork.

Reasoning:

- This is a product adaptation with different runtime behavior, not just a patch branch.
- The repo can still keep full attribution to the Claude source in `README.md`, `CHANGELOG.md`, and this plan.
- Keeping `upstream` as a remote lets us regularly pull new Claude-template changes and re-apply the Codex conversion.
- A non-fork public repo avoids GitHub UI confusion around a Claude-specific upstream when users are installing a Codex plugin.

Alternative: fork `claude-investment-assistant`, rename the fork, and adapt in place. This preserves GitHub's fork relationship but makes the plugin appear Claude-derived in GitHub navigation. Use this only if preserving fork ancestry is more important than clarity for Codex users.

## Target Repository Layout

```text
codex-investment-plugin/
├── .codex-plugin/
│   └── plugin.json
├── commands/
│   └── investment/
│       ├── setup.md
│       ├── daily.md
│       ├── new-strategy.md
│       └── help.md
├── scripts/
│   ├── workspace-bootstrap.py
│   ├── alpaca-mcp-wrapper.sh
│   └── validate-plugin.py
├── strategies/
│   ├── dip-buying.example.md
│   ├── ai-value-chain.example.md
│   └── active-trading.example.md
├── journal/
│   └── .gitkeep
├── docs/
│   ├── getting-started.md
│   ├── alpaca-setup.md
│   ├── designing-a-strategy.md
│   ├── faq.md
│   ├── safety-and-limits.md
│   ├── trading-mode.md
│   └── workspace-bootstrap.md
├── AGENTS.md
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── .gitignore
```

Notes:

- `commands/investment/*.md` should preserve the Claude command namespace shape so the intended Codex command names remain `/investment:setup`, `/investment:daily`, `/investment:new-strategy`, and `/investment:help`.
- `AGENTS.md` replaces `CLAUDE.md` as the Codex workspace guidance file.
- Keep `.claude/` out of the final repo unless we intentionally support both Claude and Codex. The user request is to change Claude to Codex.
- Keep the three example strategies functionally identical to upstream, including `status: paused` defaults.

## Phase 1: Upstream Parity Baseline

1. Confirm upstream is current:

   ```bash
   git fetch upstream main
   git rev-parse upstream/main
   ```

2. Record the upstream commit in `CHANGELOG.md` and `README.md`.
3. Keep source wording identical wherever possible.
4. Build a parity checklist:
   - `.claude/commands/investment/setup.md` -> `commands/investment/setup.md`
   - `.claude/commands/investment/daily.md` -> `commands/investment/daily.md`
   - `.claude/commands/investment/new-strategy.md` -> `commands/investment/new-strategy.md`
   - `.claude/commands/investment/help.md` -> `commands/investment/help.md`
   - `CLAUDE.md` -> `AGENTS.md`
   - `.claude/settings.json` -> Codex setup guidance plus optional `.mcp.json` if the Codex plugin runtime supports bundling MCP server declarations
5. Add a small validation script that reports any source files not yet converted.

Acceptance criteria:

- Every upstream command exists in Codex command form.
- Every upstream doc exists and has only intentional Claude-to-Codex changes.
- Example strategies diff cleanly except for references to command names or assistant runtime.

## Phase 2: Codex Command Conversion

For each command:

1. Remove Claude frontmatter such as `allowed-tools` if Codex does not use it.
2. Replace product names:
   - `Claude Code` -> `Codex`
   - `Claude` -> `Codex`
   - `claude mcp ...` -> `codex mcp ...`
   - `/mcp` references -> the Codex-equivalent MCP inspection flow
   - `.claude/commands/investment/` -> `commands/investment/`
   - `.claude/settings.json` -> Codex MCP / plugin permission setup
3. Preserve the user-facing workflow:
   - `/investment:setup` remains the setup wizard.
   - `/investment:daily` remains the daily run.
   - `/investment:new-strategy` remains the strategy builder.
   - `/investment:help` remains conversational help.
4. Update hard rules so they reflect the new two-mode system:
   - Proposal-only mode: never place trades.
   - Trading mode: may place only the confirmed orders generated by that run.
   - Setup and help commands: never place trades.
   - New-strategy command: never place trades.

Acceptance criteria:

- A repo-wide search for `Claude` returns only historical attribution or upstream comparison notes.
- A repo-wide search for `.claude` returns no runtime references.
- A repo-wide search for `claude mcp` returns no runtime setup commands.

## Phase 3: Workspace Bootstrap

Problem: a public plugin may be installed globally, but strategy and journal files are user data. The plugin needs a durable workspace path.

Implement `scripts/workspace-bootstrap.py` with this resolution order:

1. If `CODEX_INVESTMENT_WORKSPACE` is set:
   - Expand `~`.
   - Create the directory if missing.
   - Validate it is writable.
   - Use it.
2. Else if the current working directory has the marker file `.investment-assistant-workspace.json`, use the current directory.
3. Else if `~/.codex-investment-plugin/config.json` exists and contains a valid `workspace_path`, use that path.
4. Else create a default workspace:
   - macOS/Linux: `~/Documents/codex-investment-plugin-workspace`
   - Windows: `%USERPROFILE%\Documents\codex-investment-plugin-workspace`
5. Write `~/.codex-investment-plugin/config.json`:

   ```json
   {
     "workspace_path": "<absolute path>",
     "created_at": "<ISO timestamp>",
     "plugin_version": "0.1.0"
   }
   ```

6. Write `<workspace>/.investment-assistant-workspace.json`:

   ```json
   {
     "schema_version": 1,
     "workspace_type": "codex-investment-plugin",
     "created_by": "codex-investment-plugin",
     "source_upstream": "FarzamHejaziK/claude-investment-assistant",
     "source_commit": "9607f6b52214f20e340c1c27491766b78b7acc78"
   }
   ```

7. Seed the workspace if missing:
   - Copy `strategies/*.example.md` from the plugin repo.
   - Create `journal/.gitkeep`.
   - Optionally copy `docs/` as read-only reference docs or write a `README.md` that links back to the plugin docs.
8. Print the selected workspace path at the start of setup and daily runs.

Command behavior:

- `/investment:setup` must run bootstrap before asking Alpaca questions.
- `/investment:daily` must run bootstrap before reading `strategies/` or `journal/`.
- `/investment:new-strategy` must run bootstrap before validating or writing strategy files.
- `/investment:help` can run bootstrap only if the user asks about local files.

Acceptance criteria:

- Fresh plugin install with no config creates exactly one workspace and reuses it on the next run.
- Setting `CODEX_INVESTMENT_WORKSPACE` overrides the default.
- The plugin never writes user strategy or journal files into the installed plugin directory unless that directory is explicitly selected as the workspace.

## Phase 4: Alpaca Setup for Codex

Keep the same Alpaca MCP server and key-storage philosophy, translated to Codex.

Setup command changes:

1. Ask paper or live up front, same as upstream.
2. Ask execution mode:
   - `proposal-only` (recommended default): write memos and proposed orders; user places orders manually.
   - `trading-with-confirmation`: write memos, then allow user-confirmed order placement.
3. Store the execution mode in the workspace marker or config:

   ```json
   {
     "execution_mode": "proposal-only"
   }
   ```

4. Generate setup commands using Codex:

   ```bash
   codex mcp add alpaca \
     --scope user \
     --transport stdio \
     --env ALPACA_API_KEY="$(security find-generic-password -a "$USER" -s alpaca-api-key -w)" \
     --env ALPACA_SECRET_KEY="$(security find-generic-password -a "$USER" -s alpaca-secret-key -w)" \
     --env ALPACA_PAPER_TRADE=true \
     -- uvx --python 3.12 alpaca-mcp-server
   ```

5. Keep secrets out of repo files.
6. Continue supporting OS-native secure storage:
   - macOS Keychain
   - Linux `secret-tool` or `pass`
   - Windows Credential Manager
   - `.env` fallback only if clearly marked as gitignored and less preferred

Acceptance criteria:

- Setup docs contain no Claude MCP command.
- Setup verifies account with a read-only call before enabling daily runs.
- Paper/live account mismatch is detected before any trade proposal or order execution.

## Phase 5: Optional Trading Mode

Trading mode is the only intentional behavior difference from upstream.

Design principles:

- Proposal-only remains the default.
- Trading requires setup-time opt-in or an explicit later config change.
- No command places trades unless the user asks for trading mode during that run or has saved `execution_mode: trading-with-confirmation`.
- Every order batch requires an exact human confirmation before calling Alpaca order endpoints.
- The assistant only places orders derived from the active strategy files and current daily-run computation.

Daily command flow in trading mode:

1. Run the exact same analysis as proposal-only mode.
2. Write the same daily memo first, including proposed orders.
3. Build an order ticket list:

   ```json
   {
     "run_id": "YYYY-MM-DD/<hash>",
     "account_mode": "paper|live",
     "orders": [
       {
         "strategy": "dip-buying",
         "symbol": "VTI",
         "side": "buy",
         "notional": 50,
         "type": "market",
         "time_in_force": "day",
         "reason": "VTI is -5.0% from 50d high"
       }
     ]
   }
   ```

4. Preflight checks before confirmation:
   - Alpaca market clock.
   - Account mode matches configured paper/live choice.
   - Buying power / cash / SGOV funding is sufficient.
   - Quotes are fresh enough for the strategy.
   - There are no duplicate open orders for the same strategy/symbol/run.
   - The same `run_id` has not already executed.
5. Present the exact order batch and require a typed confirmation:

   ```text
   Type EXECUTE 3 ORDERS to place these orders in Alpaca.
   ```

6. Only after exact confirmation call the Alpaca order placement tool.
7. Use Alpaca order endpoints conservatively:
   - Fractional BUYs: prefer notional market orders when allowed.
   - SELLs: compute shares from held quantity and notional target; never sell more than held.
   - SGOV funding sell legs must be placed before dependent buy legs.
   - Do not submit extended-hours orders unless a strategy explicitly permits it.
8. Record results in the journal:
   - Order ID
   - Symbol
   - Side
   - Submitted quantity or notional
   - Status
   - Timestamp
   - Any rejected order error
9. If any order fails, stop the remaining dependent orders and write a clear failure note.

Commands allowed to trade:

- `/investment:daily` only.

Commands not allowed to trade:

- `/investment:setup`
- `/investment:new-strategy`
- `/investment:help`

Acceptance criteria:

- In proposal-only mode, no order placement tools are called.
- In trading mode without exact confirmation, no order placement tools are called.
- In trading mode with exact confirmation, only the displayed order batch is submitted.
- A second run on the same day does not duplicate executed orders unless the user explicitly asks for a new run and acknowledges prior execution.
- All executions are auditable in `journal/<YYYY-MM-DD>.md`.

## Phase 6: Documentation Conversion

Update docs from Claude to Codex while preserving content.

Files to update:

- `README.md`
- `docs/getting-started.md`
- `docs/alpaca-setup.md`
- `docs/designing-a-strategy.md`
- `docs/faq.md`
- `docs/safety-and-limits.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `AGENTS.md`

Add new docs:

- `docs/trading-mode.md`
- `docs/workspace-bootstrap.md`

Required documentation changes:

- Replace "template clone" assumptions with "plugin creates or uses a workspace".
- Explain where user data lives.
- Explain how to override the workspace path.
- Explain proposal-only vs trading-with-confirmation.
- Update safety doc from "not an autotrader" to "not an autonomous trader".
- Make clear that optional trading mode can place real orders in live mode.
- Keep the financial disclaimer.
- Keep example strategy warnings, especially active trading underperformance warnings.

Acceptance criteria:

- A non-programmer can install the plugin, run setup, find their workspace, and understand whether trades can be placed.
- Public README makes the trade-execution difference obvious in the first screen.
- Security doc explains how to report any unintended-trading or key-leak issue.

## Phase 7: Validation and Test Plan

Add `scripts/validate-plugin.py` to check:

- `.codex-plugin/plugin.json` parses and contains required fields.
- All expected command files exist.
- No runtime references to `.claude`, `Claude Code`, or `claude mcp` remain.
- All command names in docs match the command files.
- `strategies/*.example.md` remain paused by default.
- `journal/.gitkeep` exists.
- `.gitignore` excludes `.env`, logs, generated local state, and private workspace config.

Manual dry-run tests:

1. Fresh install, no config:
   - Run setup.
   - Confirm workspace is created.
   - Confirm examples are seeded.
2. Proposal-only paper mode:
   - Connect paper Alpaca.
   - Activate one strategy.
   - Run daily.
   - Confirm memo is written and no order tools are called.
3. Trading-with-confirmation paper mode:
   - Run daily with a strategy that creates a tiny order.
   - Confirm order ticket appears.
   - Refuse confirmation and verify no order.
   - Re-run and type exact confirmation.
   - Confirm order ID is written to journal.
4. Live mode guard:
   - Verify the prompt clearly labels live trading before confirmation.
   - Verify account mismatch blocks execution.
5. Duplicate protection:
   - Re-run the same daily command after execution.
   - Verify it detects prior order IDs and does not auto-place duplicates.

Acceptance criteria:

- All validation checks pass.
- Paper trading end-to-end works before any live-trading documentation claims are published.
- Live trading path remains confirmation-gated.

## Phase 8: Release Checklist

1. Create public GitHub repo `FarzamHejaziK/codex-investment-plugin`.
2. Set remotes:

   ```bash
   git remote add origin git@github.com:FarzamHejaziK/codex-investment-plugin.git
   git remote set-url --push upstream DISABLED
   ```

3. Commit the Codex conversion.
4. Push `main` to `origin`.
5. Tag `v0.1.0`.
6. Open a GitHub issue for each known gap.
7. Test install from the public repo.
8. Update README badges from Claude repo to Codex repo.

## Resolved Decisions

1. The public repo is Codex-only; `.claude/` is removed.
2. Trading mode is stored in workspace config, and every order batch still requires per-run exact confirmation.
3. The default workspace is `~/Documents/codex-investment-plugin-workspace`.
4. Scheduled runs are not implemented in this pass. If added later, they must remain proposal-only unless a human is present to confirm execution.
5. SGOV funding sells and target buys are treated as ordered legs, not bracket orders. Funding sells must be submitted before dependent buys.

## First Implementation Pass

Completed in this pass:

1. Create `commands/investment/` and convert the four upstream command files.
2. Add `AGENTS.md` from `CLAUDE.md`, adapted to Codex and optional trading mode.
3. Add `scripts/workspace-bootstrap.py`.
4. Update `README.md` and `docs/getting-started.md`.
5. Update `docs/safety-and-limits.md` and add `docs/trading-mode.md`.
6. Add `scripts/validate-plugin.py`.
7. Run validation.
8. Review all diffs against upstream for unintended behavior changes.
