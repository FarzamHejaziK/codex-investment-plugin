# Getting Started

This workspace is meant to be cloned and opened directly in Codex.

## 1. Clone The Workspace

```bash
git clone https://github.com/FarzamHejaziK/codex-investment-plugin.git
cd codex-investment-plugin
python3 scripts/setup-workspace.py
codex
```

The setup script creates `config/workspace.json` if it is missing and checks that `config/`, `strategies/`, and `journal/` exist.

## 2. Ask Codex To Set Up

In Codex, ask:

```text
Set up my investment workspace.
```

Codex should read `AGENTS.md`, then use `skills/setup/SKILL.md`.

Setup will ask:

- paper or live Alpaca account
- proposal-only or trading-with-confirmation
- where your Alpaca keys are stored
- which strategy examples you want to adapt

## 3. Choose Execution Mode

- **Proposal-only:** default and recommended. Codex writes memos and proposed orders; you place trades manually.
- **Trading-with-confirmation:** Codex may place only the exact displayed order batch after you type the exact confirmation phrase.

Live trading can move real money.

## 4. Activate A Strategy

The repo ships with paused examples in `strategies/`.

To activate one:

1. Copy an example to a non-example file, such as `strategies/my-dip-buying.md`.
2. Review every rule.
3. Set `status: active`.
4. Set `capital_monthly_usd` to your intended budget.

## 5. Run The Daily Checkpoint

Ask Codex:

```text
Run my daily investment checkpoint.
```

The daily workflow reads active strategies, pulls Alpaca data, writes `journal/YYYY-MM-DD.md`, and shows proposed orders.

## Next

- [Workspace](workspace.md)
- [Alpaca setup](alpaca-setup.md)
- [Trading mode](trading-mode.md)
- [Designing a strategy](designing-a-strategy.md)
- [Safety and limits](safety-and-limits.md)
