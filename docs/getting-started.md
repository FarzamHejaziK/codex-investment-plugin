# Getting started

A practical walkthrough from "I installed the plugin" to "I ran my first daily checkpoint."

## What this is

This is a Codex plugin for managing personal investment strategies. It creates or reuses a persistent workspace on your machine, stores strategy files there, connects to Alpaca through MCP, and runs a daily checkpoint.

Each daily run:

1. Reads your strategy files from `<workspace>/strategies/`
2. Pulls your Alpaca portfolio and market data
3. Calculates what your rules propose today
4. Writes a dated memo to `<workspace>/journal/`
5. Optionally submits confirmed orders if trading-with-confirmation mode is enabled

Proposal-only is the default. In proposal-only mode, Codex never places orders; you place them manually in Alpaca.

## What you need

| Thing | Why |
|---|---|
| Codex with this plugin installed | Runs the slash commands |
| Alpaca account | Provides paper or live brokerage account and market data |
| `uv` / `uvx` | Runs the Alpaca MCP server |
| About 30 minutes | One-time setup |

## The 5 steps

### 1. Install the plugin in Codex

Register the public marketplace:

```bash
codex plugin marketplace add FarzamHejaziK/codex-investment-plugin --ref main
```

Then open Codex, run `/plugins`, install **Codex Investment Assistant** from the **Codex Investment Plugin** marketplace, and start a new thread.

For local clone/development installation:

```bash
git clone https://github.com/FarzamHejaziK/codex-investment-plugin.git
cd codex-investment-plugin
codex plugin marketplace add .
```

Cloning alone does not install the plugin. Codex loads installable plugins through marketplace metadata.

### 2. Run `/investment:setup`

The setup wizard first runs `scripts/workspace-bootstrap.py`, which creates or locates your workspace. By default that workspace is:

```text
~/Documents/codex-investment-plugin-workspace
```

You can override it:

```bash
export CODEX_INVESTMENT_WORKSPACE=/path/to/my-investment-workspace
```

Then the wizard walks through Alpaca account mode, execution mode, API keys, MCP setup, and strategy configuration.

### 3. Choose execution mode

Setup asks:

- **Proposal-only (recommended):** `/investment:daily` writes memos and proposed orders. You place orders manually.
- **Trading with confirmation:** `/investment:daily` writes the memo, shows the exact order batch, and may submit that batch only after you type the exact confirmation phrase.

Live trading plus trading-with-confirmation can move real money.

### 4. Configure and activate a strategy

The workspace starts with three paused examples:

- `dip-buying.example.md`
- `ai-value-chain.example.md`
- `active-trading.example.md`

Setup can copy an example to `<name>.md`, set your monthly budget, and leave it paused or activate it. You can also edit files yourself in `<workspace>/strategies/`.

To activate manually:

1. Open `<workspace>/strategies/<name>.md`.
2. Set `status: active`.
3. Confirm `capital_monthly_usd`.
4. Save.

### 5. Run `/investment:daily`

The command:

- Reads active strategies
- Pulls Alpaca data
- Writes `<workspace>/journal/<YYYY-MM-DD>.md`
- Shows the key tables and proposed orders in chat

If proposal-only, no orders are submitted by Codex. If trading-with-confirmation is enabled, Codex still stops and asks for the exact phrase:

```text
EXECUTE <N> ORDERS
```

Anything else means no orders are placed.

## Common first-week questions

**Q: Where is my workspace?**
A: Run `python3 scripts/workspace-bootstrap.py --json` from the plugin repo, or inspect `~/.codex-investment-plugin/config.json`.

**Q: I ran `/investment:daily` and Alpaca MCP is not connected. What now?**
A: Finish or rerun `/investment:setup`, then restart Codex so the MCP server is loaded.

**Q: Paper vs. live: which should I pick?**
A: Both are supported. Paper uses simulated money. Live uses real money. If you are learning the flow, paper plus proposal-only is the lowest-risk path.

**Q: Can Codex place trades for me?**
A: Only if you choose trading-with-confirmation and confirm the exact order batch during `/investment:daily`. Setup, help, and strategy-builder commands never place trades.

**Q: What if I skip a few days?**
A: The next daily run reads prior journal entries and reconciles against Alpaca. The strategies are designed to be patient.

## Where to go next

- [Workspace bootstrap](workspace-bootstrap.md)
- [Alpaca setup](alpaca-setup.md)
- [Trading mode](trading-mode.md)
- [Designing a strategy](designing-a-strategy.md)
- [Safety and limits](safety-and-limits.md)
