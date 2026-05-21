# Changelog

All notable changes to this workspace are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Codex workspace skills in `skills/` for setup, daily checkpoint, new strategy creation, and help.
- Repo-local workspace setup script and documentation.
- Optional `trading-with-confirmation` mode for exact user-confirmed Alpaca order batches.
- Validation script for workspace shape and stale Claude/runtime references.
- `AGENTS.md` workspace guidance for Codex.
- `docs/trading-mode.md` and `docs/workspace.md`.

### Changed
- Adapted the upstream Claude Investment Assistant template to a cloned Codex workspace.
- The repo folder is now the workspace; users clone it, run `scripts/setup-workspace.py`, then work with Codex in natural language.
- The daily workflow remains proposal-only by default, with confirmed execution available only in trading-with-confirmation mode.

### Removed
- Claude-specific `.claude/` command/config directory.
- `CLAUDE.md` in favor of `AGENTS.md`.
- Plugin marketplace metadata and slash-command files in favor of workspace skills.

## [0.1.0] — 2026-05-13

Initial public template release.

### Added
- Three project-level Claude workflows for setup, daily checkpoint, and new strategy creation
- Three example strategies, all shipped as `status: paused` for safety:
  - `dip-buying.example.md` — continuous-formula dip-buying on broad ETFs
  - `ai-value-chain.example.md` — DCA basket of AI infrastructure picks-and-shovels
  - `active-trading.example.md` — daily-checkpoint mean-reversion on a curated universe
- Documentation:
  - `getting-started.md` — 15-minute walkthrough for non-programmers
  - `alpaca-setup.md` — paper/live keys, Keychain storage, MCP wiring
  - `designing-a-strategy.md` — anatomy of a strategy file
  - `faq.md`
  - `safety-and-limits.md` — propose-only design, financial disclaimer
- `.gitignore` to keep sensitive files out of git
- `.claude/settings.json` with sensible default tool permissions
