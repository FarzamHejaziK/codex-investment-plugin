#!/usr/bin/env python3
"""Validate the Codex Investment Plugin repository shape."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ".codex-plugin/plugin.json",
    "commands/investment/setup.md",
    "commands/investment/daily.md",
    "commands/investment/new-strategy.md",
    "commands/investment/help.md",
    "scripts/workspace-bootstrap.py",
    "scripts/alpaca-mcp-wrapper.sh",
    "scripts/validate-plugin.py",
    "docs/getting-started.md",
    "docs/alpaca-setup.md",
    "docs/designing-a-strategy.md",
    "docs/faq.md",
    "docs/safety-and-limits.md",
    "docs/trading-mode.md",
    "docs/workspace-bootstrap.md",
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
    "journal/.gitkeep",
    "strategies/dip-buying.example.md",
    "strategies/ai-value-chain.example.md",
    "strategies/active-trading.example.md",
]

FORBIDDEN_PATTERNS = [
    (re.compile(r"\bclaude mcp\b", re.IGNORECASE), "Claude MCP command"),
    (re.compile(r"\.claude/"), ".claude runtime path"),
    (re.compile(r"Claude Code"), "Claude Code product reference"),
]

FORBIDDEN_SKIP = {
    ".docs/plan.md",
    "CHANGELOG.md",
    "scripts/validate-plugin.py",
}


def text_files() -> list[Path]:
    ignored_parts = {".git", "docs/assets"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(str(rel).startswith(part) for part in ignored_parts):
            continue
        if path.suffix.lower() in {".md", ".json", ".py", ".sh", ".txt"} or path.name == ".gitignore":
            files.append(path)
    return files


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    manifest_path = ROOT / ".codex-plugin/plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validation should report all parse failures plainly.
        errors.append(f"plugin.json is invalid: {exc}")
        manifest = {}

    require(manifest.get("name") == "codex-investment-plugin", "plugin.json name must be codex-investment-plugin", errors)
    require(bool(manifest.get("interface", {}).get("defaultPrompt")), "plugin.json needs interface.defaultPrompt", errors)

    for rel in REQUIRED_FILES:
        require((ROOT / rel).exists(), f"missing required file: {rel}", errors)

    require(not (ROOT / ".claude").exists(), ".claude directory should not exist in Codex plugin", errors)
    require(not (ROOT / "CLAUDE.md").exists(), "CLAUDE.md should be renamed to AGENTS.md", errors)

    for strategy in (ROOT / "strategies").glob("*.example.md"):
        content = strategy.read_text(encoding="utf-8")
        require("status: paused" in content, f"{strategy.relative_to(ROOT)} must ship paused", errors)

    daily = (ROOT / "commands/investment/daily.md").read_text(encoding="utf-8")
    require("trading-with-confirmation" in daily, "daily command must document trading-with-confirmation mode", errors)
    require("EXECUTE" in daily, "daily command must require exact EXECUTE confirmation", errors)
    require("workspace-bootstrap.py" in daily, "daily command must run workspace bootstrap", errors)

    setup = (ROOT / "commands/investment/setup.md").read_text(encoding="utf-8")
    require("workspace-bootstrap.py" in setup, "setup command must run workspace bootstrap", errors)
    require("proposal-only" in setup, "setup command must configure proposal-only mode", errors)

    for path in text_files():
        rel = str(path.relative_to(ROOT))
        if rel in FORBIDDEN_SKIP:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for pattern, label in FORBIDDEN_PATTERNS:
            if pattern.search(content):
                errors.append(f"{rel} contains forbidden {label}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
