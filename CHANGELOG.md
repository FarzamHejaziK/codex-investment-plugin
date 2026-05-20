# Changelog

All notable changes to this plugin are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Codex plugin manifest in `.codex-plugin/plugin.json`.
- Codex command prompts in `commands/` with plugin namespace `investment`.
- Persistent workspace bootstrap script and documentation.
- Optional `trading-with-confirmation` mode for exact user-confirmed Alpaca order batches.
- Validation script for plugin shape and stale Claude runtime references.
- `AGENTS.md` workspace guidance for Codex.
- `docs/trading-mode.md` and `docs/workspace-bootstrap.md`.

### Changed
- Adapted the upstream Claude Investment Assistant template to Codex.
- `/investment:setup` now bootstraps the workspace and asks for execution mode.
- `/investment:daily` remains proposal-only by default, with confirmed execution available only in trading-with-confirmation mode.

### Removed
- Claude-specific `.claude/` command/config directory.
- `CLAUDE.md` in favor of `AGENTS.md`.

## [0.1.0] — 2026-05-13

Initial public template release.

### Added
- Three project-level slash commands: `/investment:setup`, `/investment:daily`, `/investment:new-strategy`
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
