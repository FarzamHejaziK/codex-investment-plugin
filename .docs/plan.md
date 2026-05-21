# Codex Investment Workspace Plan

## Direction Change

This repo should no longer be optimized as a Codex plugin marketplace package.

The new product is a **Codex-ready investment workspace**:

- A user clones the repo.
- The repo folder itself is the workspace.
- All working folders are already present in the repo.
- Reusable assistant behavior is exposed through Codex **skills**, not plugin install commands.
- Strategy files, journal files, docs, scripts, and setup state live together in the workspace unless the user intentionally moves them.

This should feel closer to the original Claude Investment Assistant workspace model, but translated cleanly to Codex.

## Implementation Status

Implemented in this repo:

- Plugin marketplace metadata was removed.
- Old slash-command files were removed.
- The command surface is now four workspace skills: `setup`, `daily`, `new-strategy`, and `help`.
- The repo root is the workspace.
- `scripts/setup-workspace.py` creates/checks local workspace files.
- `scripts/validate-workspace.py` validates the workspace shape before publishing.
- User docs now describe clone-and-open workflow, not plugin installation.

## Product Goal

Create a public repo that a user can clone and immediately open in Codex:

```bash
git clone https://github.com/FarzamHejaziK/codex-investment-plugin.git
cd codex-investment-plugin
codex
```

Inside Codex, the user should be able to ask naturally:

```text
Set up my investment workspace.
Run my daily investment checkpoint.
Create a new investment strategy.
Help me understand this workspace.
```

Codex should pick up the repo guidance and skills from the workspace and run the right workflow.

## Key Product Decisions

1. **Repo folder is the default workspace.**
   - No hidden default workspace in `~/Documents` unless the user explicitly configures one.
   - `strategies/`, `journal/`, `config/`, and `docs/` are first-class workspace folders.

2. **Skills are the main interaction model.**
   - Keep `skills/setup/SKILL.md`.
   - Keep `skills/daily/SKILL.md`.
   - Keep `skills/new-strategy/SKILL.md`.
   - Keep `skills/help/SKILL.md`.
   - Old slash-command markdown files are removed; behavior lives in the skill bodies and `AGENTS.md`.

3. **Plugin metadata becomes optional or removed.**
   - `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` are no longer the main install path.
   - They are removed entirely.
   - README should not tell normal users to run `codex plugin marketplace add`.

4. **Workspace setup should be local and obvious.**
   - The repo should include every needed folder.
   - Setup should create missing local files only when needed.
   - Secrets must never be written to the repo.

5. **Trading stays opt-in and confirmation-gated.**
   - Default remains proposal-only.
   - Direct Alpaca order execution is allowed only after the user selects trading-with-confirmation and confirms the exact displayed order batch.

## Target Workspace Layout

```text
codex-investment-plugin/
├── .docs/
│   └── plan.md
├── config/
│   ├── workspace.example.json
│   └── .gitkeep
├── docs/
│   ├── getting-started.md
│   ├── alpaca-setup.md
│   ├── designing-a-strategy.md
│   ├── faq.md
│   ├── safety-and-limits.md
│   ├── trading-mode.md
│   └── workspace.md
├── journal/
│   └── .gitkeep
├── scripts/
│   ├── alpaca-mcp-wrapper.sh
│   ├── setup-workspace.py
│   └── validate-workspace.py
├── skills/
│   ├── setup/
│   │   └── SKILL.md
│   ├── daily/
│   │   └── SKILL.md
│   ├── new-strategy/
│   │   └── SKILL.md
│   └── help/
│       └── SKILL.md
├── strategies/
│   ├── dip-buying.example.md
│   ├── ai-value-chain.example.md
│   └── active-trading.example.md
├── AGENTS.md
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── .gitignore
```

## Phase 1: Reframe The Repo

1. Rename the public-facing concept from "plugin" to "workspace" everywhere:
   - README
   - docs
   - AGENTS.md
   - script names and comments
   - validation output
2. Decide whether to rename the GitHub repo later.
   - Current repo can stay `codex-investment-plugin` for continuity.
   - README should still say this is now a workspace repo.
3. Remove normal-user plugin installation instructions.
4. Replace install flow with:

   ```bash
   git clone https://github.com/FarzamHejaziK/codex-investment-plugin.git
   cd codex-investment-plugin
   codex
   ```

Acceptance criteria:

- README no longer says users must install via `/plugins`.
- A new user understands that cloning the repo is the install step.
- `plugin` only appears in historical attribution, legacy notes, or if the repo name is mentioned.

## Phase 2: Make Skills The Command Surface

1. Treat `skills/` as the primary behavior layer.
2. Expand each skill so it is self-contained enough to run without loading old `commands/*.md`.
3. Keep the four user workflows:
   - setup
   - daily checkpoint
   - new strategy builder
   - help and troubleshooting
4. Update AGENTS.md to tell Codex to use these skills for matching requests.
5. Do not keep slash-command wrappers in the repo.

Acceptance criteria:

- `AGENTS.md` routes natural-language investment requests to the matching `skills/*/SKILL.md` file.
- The user can type natural language instead of remembering slash commands.
- Skills reference workspace-local files with clear relative paths.

## Phase 3: Workspace-Local Setup

Replace `scripts/workspace-bootstrap.py` with `scripts/setup-workspace.py`.

Behavior:

1. Treat the repo root as the workspace when it contains `AGENTS.md`, `skills/`, `strategies/`, and `journal/`.
2. Create missing folders:
   - `config/`
   - `journal/`
   - `strategies/`
3. Create `config/workspace.json` from `config/workspace.example.json` if missing.
4. Never write API keys into `config/`.
5. Record local settings only:

   ```json
   {
     "schema_version": 1,
     "workspace_type": "codex-investment-workspace",
     "execution_mode": "proposal-only",
     "alpaca_account_mode": null,
     "created_at": "<ISO timestamp>"
   }
   ```

6. Keep examples in `strategies/*.example.md`.
7. New user strategy files are created as `strategies/<name>.md`.

Acceptance criteria:

- Running setup from the repo does not create `~/Documents/codex-investment-plugin-workspace`.
- Running setup twice is idempotent.
- The repo has all user-visible working folders from the beginning.

## Phase 4: Alpaca Setup

Keep the Alpaca MCP approach, but document it as workspace setup rather than plugin setup.

Setup skill should:

1. Ask paper or live.
2. Ask proposal-only or trading-with-confirmation.
3. Store only non-secret choices in `config/workspace.json`.
4. Store secrets in the OS keychain or user-managed environment, never in the repo.
5. Register the Alpaca MCP through Codex user config.
6. Verify with read-only account calls before any daily run.

Acceptance criteria:

- The setup skill can guide a non-programmer from clone to connected Alpaca MCP.
- Paper/live mismatch is detected before proposals.
- No secret values appear in git-tracked files.

## Phase 5: Daily Checkpoint

The daily skill should:

1. Run workspace setup/check first.
2. Read `config/workspace.json`.
3. Read active files from `strategies/*.md`.
4. Pull Alpaca account state and market data through MCP.
5. Write a dated memo under `journal/YYYY-MM-DD.md`.
6. Propose orders according to strategy rules.
7. In proposal-only mode, stop there.
8. In trading-with-confirmation mode, show the exact order batch and require:

   ```text
   EXECUTE <N> ORDERS
   ```

Acceptance criteria:

- No active strategies means a clear stop message.
- Proposal-only mode never places trades.
- Trading mode cannot submit undisplayed or modified orders.

## Phase 6: Strategy Builder

The new-strategy skill should:

1. Ask one question at a time.
2. Generate a complete strategy file under `strategies/<name>.md`.
3. Default every new strategy to `status: paused`.
4. Include frontmatter, allowed instruments, budget, sizing, risk rules, and review cadence.
5. Tell the user exactly how to activate the strategy.

Acceptance criteria:

- The builder never creates active strategies by surprise.
- The output is readable markdown, not hidden config.
- The daily skill can parse the generated file without special cases.

## Phase 7: Documentation Rewrite

Update docs for the workspace model:

1. `docs/getting-started.md`
   - clone repo
   - open Codex
   - ask setup skill to run
2. `docs/workspace.md`
   - explain folders and local config
3. `docs/alpaca-setup.md`
   - Codex MCP setup
4. `docs/trading-mode.md`
   - confirmation-gated execution
5. `docs/faq.md`
   - no plugin install flow
   - how to update the repo with `git pull`

Acceptance criteria:

- A user can follow docs without knowing what a Codex plugin marketplace is.
- Slash commands are not required to understand or run the system.

## Phase 8: Validation

Replace plugin validation with workspace validation.

`scripts/validate-workspace.py` should check:

- required folders exist
- required skills exist and have valid frontmatter
- required strategy examples exist and ship paused
- `config/workspace.example.json` is valid JSON
- no secret-looking values are committed
- no stale Claude runtime references remain
- no normal-user docs still say to install via `/plugins`

Acceptance criteria:

- `python3 scripts/validate-workspace.py` passes on a fresh clone.
- Validation fails if a strategy example ships active.
- Validation fails if docs point users to plugin marketplace install as the primary path.

## Phase 9: Migration From Current Repo

Concrete migration steps from the current plugin version:

1. Move or remove plugin marketplace files:
   - `.codex-plugin/plugin.json`
   - `.agents/plugins/marketplace.json`
2. Remove command markdown after merging behavior into `skills/*/SKILL.md`.
3. Rename scripts:
   - `workspace-bootstrap.py` -> `setup-workspace.py`
   - `validate-plugin.py` -> `validate-workspace.py`
4. Add `config/` with examples.
5. Update README and docs.
6. Run validation.
7. Commit and push.

## Open Questions

1. Should the GitHub repo eventually be renamed from `codex-investment-plugin` to `codex-investment-workspace`?
2. Should user-created strategy and journal files be committed by default, or should `.gitignore` exclude non-example strategy files and journal entries for privacy?

## Recommended Next Implementation

Start with the smallest useful conversion:

1. Update README and docs to say this is a workspace.
2. Add `config/workspace.example.json`.
3. Rename validation to `validate-workspace.py`.
4. Make setup use repo root by default.
5. Expand skills so they are self-contained.
6. Remove plugin install instructions from the normal path.

After that, test from a fresh clone:

```bash
git clone https://github.com/FarzamHejaziK/codex-investment-plugin.git /tmp/codex-investment-workspace-test
cd /tmp/codex-investment-workspace-test
python3 scripts/validate-workspace.py
python3 scripts/setup-workspace.py --json
```
