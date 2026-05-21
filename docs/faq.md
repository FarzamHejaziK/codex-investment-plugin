# FAQ

## Do I install this as a Codex workspace?

No. Clone the repo and open it in Codex. The repo is the workspace.

## What should I ask Codex?

Use natural language:

- "Set up my investment workspace."
- "Run my daily investment checkpoint."
- "Create a new investment strategy."
- "Help me understand this workspace."

## Where is my workspace?

The cloned repo folder is the workspace. Run:

```bash
python3 scripts/setup-workspace.py --json
```

## Can Codex place trades?

Not by default. Proposal-only mode never places orders. Trading-with-confirmation can place orders only after Codex displays the exact batch and you type `EXECUTE <N> ORDERS`.

## Where do API keys live?

Outside the repo. Use macOS Keychain, Linux secret storage, Windows Credential Manager, or another user-managed secret store.

## Why are examples paused?

Examples are templates, not recommendations. You must review, copy, edit, and activate a strategy yourself.

## How do I update the workspace?

Commit or stash local changes, then run:

```bash
git pull
```

Be careful if you commit personal strategy or journal files to a public fork.
