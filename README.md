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

[About](#about) - [Quick Start](#quick-start) - [Alpaca MCP](#alpaca-mcp-setup) - [Workspace](docs/workspace.md) - [Docs](#documentation) - [Safety](docs/safety-and-limits.md)

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

## Alpaca MCP Setup

The daily workflow uses the Alpaca MCP server to read account state, positions, orders, quotes, and bars. In proposal-only mode it never places orders. In `trading-with-confirmation` mode it may place only the exact order batch you confirm.

### 1. Create Alpaca API keys

Use paper first:

1. Open <https://app.alpaca.markets/paper/dashboard/overview>.
2. Find **API Keys**.
3. Generate a new key.
4. Copy the Key ID and Secret Key immediately.

For live trading, use <https://app.alpaca.markets/live/dashboard/overview>. Live keys can move real money when trading-with-confirmation is enabled and confirmed.

Paper keys normally start with `PK`; live keys normally start with `AK`. Match that with `ALPACA_PAPER_TRADE=true` for paper or `ALPACA_PAPER_TRADE=false` for live.

### 2. Store keys outside the repo

Never commit API keys to this repo, strategy files, journal files, docs, or chat.

On macOS, store them in Keychain:

```bash
read -s "k?Paste ALPACA_API_KEY: " && echo && \
  security add-generic-password -a "$USER" -s alpaca-api-key -w "$k" -U && unset k

read -s "s?Paste ALPACA_SECRET_KEY: " && echo && \
  security add-generic-password -a "$USER" -s alpaca-secret-key -w "$s" -U && unset s
```

Quick verification without printing secrets:

```bash
echo "API key prefix: $(security find-generic-password -a "$USER" -s alpaca-api-key -w | cut -c1-2)"
echo "Secret length: $(security find-generic-password -a "$USER" -s alpaca-secret-key -w | wc -c)"
```

On Linux, use `secret-tool` or `pass`. On Windows, use Credential Manager. See [Alpaca setup](docs/alpaca-setup.md) for those examples.

### 3. Install `uv`

The MCP server is launched with `uvx`:

```bash
# macOS
brew install uv

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install Python 3.12:

```bash
uv python install 3.12
```

### 4. Add the Alpaca MCP server to Codex

Recommended macOS wrapper setup from this repo:

```bash
codex mcp add alpaca \
  --env ALPACA_PAPER_TRADE=true \
  -- "$(pwd)/scripts/alpaca-mcp-wrapper.sh"
```

Use `ALPACA_PAPER_TRADE=false` only for live keys.

Direct setup without the wrapper:

```bash
codex mcp add alpaca \
  --env ALPACA_API_KEY="$(security find-generic-password -a "$USER" -s alpaca-api-key -w)" \
  --env ALPACA_SECRET_KEY="$(security find-generic-password -a "$USER" -s alpaca-secret-key -w)" \
  --env ALPACA_PAPER_TRADE=true \
  -- uvx --python 3.12 alpaca-mcp-server
```

### 5. Verify and restart Codex

```bash
codex mcp list
```

You should see an `alpaca` server. Restart Codex after adding or changing MCP configuration so the tools load into the session.

To switch between paper and live:

```bash
codex mcp remove alpaca
```

Then re-add it with the matching keys and `ALPACA_PAPER_TRADE` value.

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
