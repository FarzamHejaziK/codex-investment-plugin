<div align="center">

<img src="docs/assets/logo.png" alt="Codex Investment Assistant" width="520" />

# codex-investment-plugin

**A Codex-ready investment workspace for designing, tracking, and running personal Alpaca strategies.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/FarzamHejaziK/codex-investment-plugin?style=social)](https://github.com/FarzamHejaziK/codex-investment-plugin/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/FarzamHejaziK/codex-investment-plugin)](https://github.com/FarzamHejaziK/codex-investment-plugin/commits/main)
[![Open issues](https://img.shields.io/github/issues/FarzamHejaziK/codex-investment-plugin)](https://github.com/FarzamHejaziK/codex-investment-plugin/issues)
[![Built for Codex](https://img.shields.io/badge/built%20for-Codex-blue)](https://openai.com/codex)
[![Powered by Alpaca](https://img.shields.io/badge/powered%20by-Alpaca-purple)](https://alpaca.markets/)

[About](#about) - [Quick Start](#quick-start) - [Workspace](docs/workspace.md) - [Docs](#documentation) - [Safety](docs/safety-and-limits.md)

</div>

---

## About

`codex-investment-plugin` is now a cloned Codex workspace. The repo folder is the workspace: it contains the strategy files, journal folder, local config example, docs, scripts, and Codex skill instructions.

It ships with three paused example strategies: dip-buying, AI value-chain DCA, and mean-reversion active trading. You can adapt them or ask Codex to create a new strategy.

The default mode is **proposal-only**. Codex writes daily memos and proposed orders; you place any trades yourself. Optional `trading-with-confirmation` mode can submit Alpaca orders only after Codex shows the exact batch and you type the exact confirmation phrase.

> This is not financial advice. This workspace helps organize and execute your own rules. Live trading can move real money.

## Quick Start

```bash
git clone https://github.com/FarzamHejaziK/codex-investment-plugin.git
cd codex-investment-plugin
python3 scripts/setup-workspace.py
codex
```

Then ask Codex:

```text
Set up my investment workspace.
```

Codex should follow `AGENTS.md` and the local skills in `skills/`.

## What It Does

1. Keeps your strategies as markdown files under `strategies/`.
2. Keeps daily memos and execution records under `journal/`.
3. Stores non-secret local settings in `config/workspace.json`.
4. Uses Alpaca MCP for account, position, activity, quote, bar, and optional order tools.
5. Provides four skill workflows:
   - `setup`
   - `daily`
   - `new-strategy`
   - `help`

## File Layout

```text
codex-investment-plugin/
├── config/
│   └── workspace.example.json
├── docs/
├── journal/
│   └── .gitkeep
├── scripts/
│   ├── setup-workspace.py
│   ├── alpaca-mcp-wrapper.sh
│   └── validate-workspace.py
├── skills/
│   ├── setup/
│   ├── daily/
│   ├── new-strategy/
│   └── help/
├── strategies/
│   ├── dip-buying.example.md
│   ├── ai-value-chain.example.md
│   └── active-trading.example.md
├── AGENTS.md
└── README.md
```

## Example Strategies

| File | Style | Risk |
|---|---|---|
| `strategies/dip-buying.example.md` | Buy-only broad ETF dip-buying | Low |
| `strategies/ai-value-chain.example.md` | AI infrastructure DCA basket | Medium |
| `strategies/active-trading.example.md` | Mean-reversion active trading | High |

All examples ship with `status: paused`.

## Documentation

- [Getting started](docs/getting-started.md)
- [Workspace](docs/workspace.md)
- [Alpaca setup](docs/alpaca-setup.md)
- [Trading mode](docs/trading-mode.md)
- [Designing a strategy](docs/designing-a-strategy.md)
- [FAQ](docs/faq.md)
- [Safety and limits](docs/safety-and-limits.md)

## Source Attribution

This workspace is adapted from [FarzamHejaziK/claude-investment-assistant](https://github.com/FarzamHejaziK/claude-investment-assistant), with the runtime changed from Claude-oriented commands to Codex workspace skills.

## License

MIT. See [LICENSE](LICENSE).
