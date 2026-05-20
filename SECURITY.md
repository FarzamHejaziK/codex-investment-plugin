# Security policy

This plugin can access brokerage account data through Alpaca MCP and can optionally submit confirmed orders. Security issues matter.

## Sensitive assets

- Alpaca API keys
- Brokerage account data
- Strategy files
- Journal memos and order IDs
- Workspace config files

Keys must live in OS secret storage or explicitly provided environment variables. They must not be committed to this repo or written into the workspace.

## Highest-impact issues

- API key leakage
- Unintended order placement
- Bypassing the `EXECUTE <N> ORDERS` confirmation
- Submitting orders that were not displayed to the user
- Paper/live account mismatch that causes live trading when paper was intended
- Tampering with strategy files or journal audit records

## Reporting a vulnerability

Do not file a public issue for security problems. Use GitHub Security Advisories on this repo, or contact `@FarzamHejaziK` and request a private channel.

Include:

- Impact
- Reproduction steps
- Commit SHA
- Whether paper, live, or both are affected
- Logs or screenshots with secrets redacted

## Not security issues

- Losing money because a user-authored strategy performs poorly
- A disagreement with a strategy's investing premise
- A rejected or partially filled market order caused by normal market behavior

Those can still be normal bugs or documentation issues.

## User recommendations

- Start with paper mode.
- Start with proposal-only mode.
- Keep your workspace private.
- Rotate Alpaca keys after any suspected exposure.
- Review `docs/trading-mode.md` before enabling confirmed execution.
