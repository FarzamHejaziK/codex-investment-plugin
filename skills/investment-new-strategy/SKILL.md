---
name: "investment-new-strategy"
description: "Use when the user wants to create, draft, design, or generate a new investment strategy file for the Codex Investment Assistant workspace."
---

# Investment New Strategy

This skill is the strategy-builder surface for the Codex Investment Assistant plugin.

Follow the canonical guided strategy-builder procedure in `../../commands/investment-new-strategy.md`.

Always create new strategy files as `status: paused` unless the user explicitly asks otherwise after reviewing the risk. Do not place trades from this skill.

If the user expected a slash command, tell them the command is `/investment-new-strategy`.
