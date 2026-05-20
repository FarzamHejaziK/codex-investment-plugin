# FAQ

## Setup & basics

**Q: Do I need to know how to code?**
A: No. You need to run setup, answer questions, and occasionally edit markdown strategy files.

**Q: Where does my data live?**
A: In the workspace resolved by `scripts/workspace-bootstrap.py`, usually `~/Documents/codex-investment-plugin-workspace`. Run `python3 scripts/workspace-bootstrap.py --json` to inspect it.

**Q: What brokers does this work with?**
A: Alpaca only, out of the box. Other brokers would require new connector and strategy reconciliation work.

**Q: Paper or live?**
A: Both are supported. Paper is simulated. Live is real money. The `ALPACA_PAPER_TRADE` MCP setting must match the key prefix: `PK + true`, `AK + false`.

## Trading & safety

**Q: Will this place trades automatically?**
A: Not by default. Proposal-only mode never places orders. Trading-with-confirmation can place orders only during `/investment:daily`, after Codex shows the exact batch and you type `EXECUTE <N> ORDERS`.

**Q: Which commands can place trades?**
A: Only `/investment:daily`, and only in trading-with-confirmation mode. `/investment:setup`, `/investment:new-strategy`, and `/investment:help` never place trades.

**Q: Can I use trading-with-confirmation with live money?**
A: Yes, but be careful. If live Alpaca credentials are connected, confirmed orders affect the real account. Test with paper first.

**Q: Is this financial advice?**
A: No. The plugin follows your strategy files. You own every investment decision.

**Q: Can I lose all my money?**
A: In paper mode no, because it is simulated. In live mode yes, any investment can lose principal. Active trading is especially risky.

## Strategy questions

**Q: How often should I run `/investment:daily`?**
A: Once per market day is the intended rhythm. More frequent runs usually add noise unless your strategy says otherwise.

**Q: Can I run multiple strategies?**
A: Yes. Each active strategy has its own `capital_monthly_usd`. Use non-overlapping universes when possible to avoid one strategy interfering with another.

**Q: How do I pause a strategy?**
A: Open `<workspace>/strategies/<name>.md`, change `status: active` to `status: paused`, and save.

**Q: Can a strategy buy options or crypto?**
A: Only if you write explicit strategy rules for those instruments and the Alpaca MCP supports the needed endpoints. The included examples are equities/ETFs only.

## File and data questions

**Q: Should I commit my workspace to git?**
A: Your call. If it contains real portfolio data or trade history, keep it private. Journal files can reveal sensitive financial information.

**Q: Can I edit old journal entries?**
A: Avoid it. Journal entries are an audit trail. Add corrections in a later memo.

**Q: What does "Strategy notes" mean?**
A: It is where `/investment:daily` surfaces possible strategy changes. Codex should not auto-edit operational strategy sections.

## Troubleshooting

**Q: `/investment:daily` says no active strategies.**
A: Open `<workspace>/strategies/` and set at least one non-example strategy file to `status: active`.

**Q: Alpaca returns HTTP 401.**
A: Usually paper/live mismatch. See [Alpaca setup](alpaca-setup.md).

**Q: The daily memo position data is wrong.**
A: Check Alpaca directly, then check whether you placed orders outside the memo. The daily run should flag reconciliation drift.

**Q: Slash commands are missing.**
A: Restart Codex and confirm the plugin repo contains `commands/*.md`. The plugin manifest name is `investment`, so the intended commands are `/investment:setup`, `/investment:daily`, `/investment:new-strategy`, and `/investment:help`.

**Q: Can I ask general questions without a command?**
A: Yes. `AGENTS.md` gives Codex the workspace context.
