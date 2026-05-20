# Safety and limits

This doc covers what the plugin will and will not do, why the defaults are conservative, and what changes when you enable trading-with-confirmation.

## What this tool is

A Codex plugin for organizing investment strategies. `/investment:daily` reads strategy files, pulls Alpaca portfolio data, writes a daily memo, and proposes specific orders based on rules you wrote.

## What this tool is not

- **Not financial advice.** It follows your strategy files; it does not decide what is suitable for you.
- **Not a robo-advisor.** There is no suitability review, fiduciary duty, or licensed advisor behind it.
- **Not an autonomous trader.** It does not independently decide to trade. Trading mode still requires explicit per-run confirmation.
- **Not regulated investment software.** It is MIT-licensed open-source software.

## Execution modes

### Proposal-only

This is the default and recommended mode.

1. Strategy files declare rules.
2. `/investment:daily` proposes orders and writes the memo.
3. You place orders manually in Alpaca if you agree.

Codex does not call Alpaca order-placement tools in this mode.

### Trading-with-confirmation

This is optional.

1. `/investment:daily` runs the same analysis and writes the same memo.
2. Codex builds an exact order batch from the memo.
3. Codex runs preflight checks.
4. Codex shows the exact batch in chat.
5. You must type `EXECUTE <N> ORDERS`.
6. Codex submits only that displayed batch.
7. Codex appends Alpaca order IDs and statuses to the journal.

Anything other than the exact confirmation phrase means no orders are placed.

## What can go wrong

- **Bad strategies can lose money.** The plugin follows your rules. It does not prove those rules are profitable.
- **Live mode can move real money.** If live Alpaca credentials are configured and trading-with-confirmation is enabled, confirmed orders affect the live account.
- **Order execution can differ from proposal math.** Market orders can fill at different prices, partially fill, or be rejected.
- **API outages happen.** If Alpaca or MCP is unavailable, the daily run must stop rather than fabricate data.
- **Journal drift can happen.** If you place trades outside the proposed batch, the strategy ledger may no longer match Alpaca. The daily run should flag this.
- **Short-term trading has tax drag.** Active-trading strategies can create ordinary-income-rate gains and wash-sale complexity.

## Specific strategy risks

### Dip-buying

- A dip can become a crash.
- Buy-only rules can keep accumulating into a drawdown.
- Monthly caps can be exhausted before the bottom.

### DCA basket

- Theme baskets can be more correlated than they look.
- A stale watchlist can keep buying broken theses.
- Equal weighting does not remove single-name risk.

### Active trading

- Retail active traders often underperform simple indexes.
- Stop losses and time stops can still lose repeatedly.
- The strategy may need many trades before results are statistically meaningful.
- Taxes and behavior can dominate any theoretical edge.

## Hard safety rules

- Setup, help, and strategy-builder commands never place trades.
- `/investment:daily` is the only command that may place orders, and only in trading-with-confirmation mode.
- Codex must write the memo before requesting execution confirmation.
- Codex must show the exact order batch before requesting confirmation.
- Codex must not submit instruments outside the strategy file's allowed universe.
- Codex must not submit undisplayed orders.
- Codex must record submitted order IDs in the journal.
- Codex must never store API keys in repo, workspace, strategy, journal, or chat content.

## If something feels wrong

Stop. Do not confirm execution. Use proposal-only mode until you understand the behavior.

Report bugs at <https://github.com/FarzamHejaziK/codex-investment-plugin/issues>. Report security issues privately according to [SECURITY.md](../SECURITY.md), especially anything involving key leakage or unintended order placement.

## Financial disclaimer

This software is not financial advice. Investment decisions are your responsibility. Past performance does not guarantee future results. All investments carry risk, including the risk of partial or total loss of principal.

The author is not a licensed financial advisor. Example strategies are educational and illustrative, not endorsements of any particular trading approach or security.
