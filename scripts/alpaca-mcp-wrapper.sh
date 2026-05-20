#!/usr/bin/env bash
set -euo pipefail

# Convenience wrapper for Codex MCP setup. It prefers explicit environment
# variables, then falls back to macOS Keychain entries used by the setup guide.

if [[ -z "${ALPACA_API_KEY:-}" ]] && command -v security >/dev/null 2>&1; then
  ALPACA_API_KEY="$(security find-generic-password -a "$USER" -s alpaca-api-key -w 2>/dev/null || true)"
  export ALPACA_API_KEY
fi

if [[ -z "${ALPACA_SECRET_KEY:-}" ]] && command -v security >/dev/null 2>&1; then
  ALPACA_SECRET_KEY="$(security find-generic-password -a "$USER" -s alpaca-secret-key -w 2>/dev/null || true)"
  export ALPACA_SECRET_KEY
fi

if [[ -z "${ALPACA_API_KEY:-}" || -z "${ALPACA_SECRET_KEY:-}" ]]; then
  echo "Missing ALPACA_API_KEY or ALPACA_SECRET_KEY. Run /investment-setup first." >&2
  exit 1
fi

export ALPACA_PAPER_TRADE="${ALPACA_PAPER_TRADE:-true}"
exec uvx --python 3.12 alpaca-mcp-server "$@"
