# Alpaca setup

This doc covers opening an Alpaca account, generating API keys, storing them securely, wiring up the Codex MCP connection, and switching between paper and live.

For first-time setup, run `/investment-setup` in Codex. Use this doc when something goes wrong or when you want to rotate keys.

## Paper vs. live

| | Paper | Live |
|---|---|---|
| Money | Simulated balance | Real money you deposit |
| Risk | No financial loss | You can lose principal |
| API endpoint | `https://paper-api.alpaca.markets` | `https://api.alpaca.markets` |
| API key prefix | `PK...` | `AK...` |
| `ALPACA_PAPER_TRADE` | `true` | `false` |

Both are supported. The key prefix and `ALPACA_PAPER_TRADE` value must match.

## Generate API keys

Paper:

1. Go to <https://app.alpaca.markets/paper/dashboard/overview>.
2. Find **API Keys**.
3. Click **Generate New Key**.
4. Copy both the Key ID and Secret Key immediately.

Live:

1. Go to <https://app.alpaca.markets/live/dashboard/overview>.
2. Repeat the same key-generation flow.
3. Confirm you understand live credentials can move real money if trading-with-confirmation is enabled and confirmed.

The Secret Key is shown only once. If you lose it, generate a new key pair.

## Store keys securely

Never commit keys to this repo, your workspace, strategy files, or journal entries.

### macOS Keychain

Run these in your own terminal:

```bash
read -s "k?Paste ALPACA_API_KEY: " && echo && \
  security add-generic-password -a "$USER" -s alpaca-api-key -w "$k" -U && unset k

read -s "s?Paste ALPACA_SECRET_KEY: " && echo && \
  security add-generic-password -a "$USER" -s alpaca-secret-key -w "$s" -U && unset s
```

Verify without printing the full values:

```bash
echo "API key prefix: $(security find-generic-password -a "$USER" -s alpaca-api-key -w | cut -c1-2)"
echo "Secret length: $(security find-generic-password -a "$USER" -s alpaca-secret-key -w | wc -c)"
```

### Linux

Use `secret-tool` or `pass`. Example with `secret-tool`:

```bash
secret-tool store --label="Alpaca API key" service alpaca-api-key
secret-tool store --label="Alpaca Secret" service alpaca-secret-key
```

### Windows

Use Credential Manager. In PowerShell:

```powershell
Install-Module -Name CredentialManager -Scope CurrentUser -Force
New-StoredCredential -Target "alpaca-api-key" -Username "$env:USERNAME" -Password (Read-Host -AsSecureString)
New-StoredCredential -Target "alpaca-secret-key" -Username "$env:USERNAME" -Password (Read-Host -AsSecureString)
```

### `.env` fallback

Only use this when OS secret storage is unavailable. The repo ignores `.env`.

```bash
ALPACA_API_KEY=PKxxxxxxxxxxxxxxxxx
ALPACA_SECRET_KEY=your_long_secret_here
```

Source it before adding the MCP.

## Install `uv`

```bash
# macOS
brew install uv

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install Python:

```bash
uv python install 3.12
```

## Wire up the MCP

### Direct `uvx` command

Paper:

```bash
codex mcp add alpaca \
  --scope user \
  --transport stdio \
  --env ALPACA_API_KEY="$(security find-generic-password -a "$USER" -s alpaca-api-key -w)" \
  --env ALPACA_SECRET_KEY="$(security find-generic-password -a "$USER" -s alpaca-secret-key -w)" \
  --env ALPACA_PAPER_TRADE=true \
  -- uvx --python 3.12 alpaca-mcp-server
```

Live:

```bash
codex mcp add alpaca \
  --scope user \
  --transport stdio \
  --env ALPACA_API_KEY="$(security find-generic-password -a "$USER" -s alpaca-api-key -w)" \
  --env ALPACA_SECRET_KEY="$(security find-generic-password -a "$USER" -s alpaca-secret-key -w)" \
  --env ALPACA_PAPER_TRADE=false \
  -- uvx --python 3.12 alpaca-mcp-server
```

### Plugin wrapper command

The wrapper reads macOS Keychain if explicit env vars are absent:

```bash
codex mcp add alpaca \
  --scope user \
  --transport stdio \
  --env ALPACA_PAPER_TRADE=true \
  -- /absolute/path/to/codex-investment-plugin/scripts/alpaca-mcp-wrapper.sh
```

Use `ALPACA_PAPER_TRADE=false` for live keys.

## Verify

```bash
codex mcp list
```

Expected: `alpaca` is connected. Restart Codex after adding or changing MCP configuration.

During `/investment-setup`, Codex should call `mcp__alpaca__get_account_info` and show only safe account details such as last four account digits, equity, buying power, and cash.

## Switch paper/live

1. Generate keys in the other Alpaca panel.
2. Update secure storage.
3. Remove and re-add the MCP with the matching `ALPACA_PAPER_TRADE` value.
4. Restart Codex.

Mismatch symptoms: `get_clock` works but account calls return HTTP 401. Fix by matching `PK + true` or `AK + false`.

## Troubleshooting

**MCP failed to start**
Run:

```bash
uvx --python 3.12 alpaca-mcp-server --help
```

If Python inspection fails, rerun `uv python install 3.12`.

**Tools are unavailable in Codex**
Restart Codex. MCP tools load at session start.

**You pasted a key into chat**
Regenerate the key in Alpaca, update secure storage, and re-add the MCP. Treat the pasted key as compromised.
