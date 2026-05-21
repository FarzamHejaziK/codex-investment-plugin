# Trading mode

Trading-with-confirmation is the optional mode that lets the daily workflow submit Alpaca orders after explicit user confirmation.

Proposal-only is still the default. Use trading-with-confirmation only after you are comfortable with paper runs and the strategy files.

## Enable it

During the setup workflow, choose:

```text
Trading with confirmation
```

Or update the workspace config from the workspace repo:

```bash
python3 scripts/setup-workspace.py --execution-mode trading-with-confirmation
```

Switch back:

```bash
python3 scripts/setup-workspace.py --execution-mode proposal-only
```

The setting is stored in `config/workspace.json`.

## Daily run flow

1. The daily workflow checks the workspace.
2. It reads active strategies.
3. It pulls Alpaca account state and market data.
4. It writes the journal memo.
5. It builds an order ticket list from the memo's proposed orders.
6. It runs preflight checks.
7. It shows the exact order batch.
8. It asks for:

   ```text
   EXECUTE <N> ORDERS
   ```

9. If the phrase matches exactly, it submits the displayed orders.
10. It appends order IDs and statuses to the same journal memo.

Anything other than the exact phrase stops execution.

## Preflight checks

Codex must check:

- Paper/live account mode
- Alpaca market clock and calendar
- Cash, buying power, and SGOV funding reserve
- Freshness of quotes
- Existing open orders
- Duplicate execution for the same daily run
- Strategy buy/sell scope

If a check fails, no orders should be submitted.

## Live account warning

If `ALPACA_PAPER_TRADE=false`, confirmed orders affect your real Alpaca account. Market orders can fill at worse prices than expected, partially fill, or be rejected.

Use paper first.

## What commands can trade?

Only the daily workflow.

These never trade:

- setup workflow
- new-strategy workflow
- help workflow

## Audit trail

Every confirmed execution should append:

- Run ID
- Confirmation phrase
- Strategy
- Symbol
- Side
- Notional or quantity
- Alpaca order ID
- Status
- Notes or errors

The journal is the audit trail. Do not rewrite old journal entries; add corrections in a later memo.
