#!/usr/bin/env python3
"""Validate the Codex Investment Plugin repository shape."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ".agents/plugins/marketplace.json",
    ".codex-plugin/plugin.json",
    "commands/investment-setup.md",
    "commands/investment-daily.md",
    "commands/investment-new-strategy.md",
    "commands/investment-help.md",
    "skills/investment-setup/SKILL.md",
    "skills/investment-daily/SKILL.md",
    "skills/investment-new-strategy/SKILL.md",
    "skills/investment-help/SKILL.md",
    "scripts/workspace-bootstrap.py",
    "scripts/alpaca-mcp-wrapper.sh",
    "scripts/validate-plugin.py",
    "docs/getting-started.md",
    "docs/installation.md",
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

    require(manifest.get("name") == "investment", "plugin.json name must be investment", errors)
    require(manifest.get("version") == "0.1.1", "plugin.json version must be 0.1.1", errors)
    require(manifest.get("skills") == "./skills/", "plugin.json must expose ./skills/", errors)
    require(bool(manifest.get("interface", {}).get("defaultPrompt")), "plugin.json needs interface.defaultPrompt", errors)

    marketplace_path = ROOT / ".agents/plugins/marketplace.json"
    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validation should report all parse failures plainly.
        errors.append(f"marketplace.json is invalid: {exc}")
        marketplace = {}

    plugins = marketplace.get("plugins", [])
    investment_entries = [entry for entry in plugins if entry.get("name") == "investment"]
    require(marketplace.get("name") == "codex-investment-plugin", "marketplace name must be codex-investment-plugin", errors)
    require(len(investment_entries) == 1, "marketplace must expose exactly one investment plugin entry", errors)
    if investment_entries:
        entry = investment_entries[0]
        source = entry.get("source", {})
        require(source.get("source") == "url", "marketplace investment source must use url for repo-root plugin", errors)
        require(
            source.get("url") == "https://github.com/FarzamHejaziK/codex-investment-plugin.git",
            "marketplace investment source url is wrong",
            errors,
        )
        require(source.get("ref") == "main", "marketplace investment source ref must be main", errors)
        require(entry.get("policy", {}).get("installation") == "AVAILABLE", "marketplace installation policy must be AVAILABLE", errors)
        require(entry.get("policy", {}).get("authentication") == "ON_INSTALL", "marketplace auth policy must be ON_INSTALL", errors)
        require(entry.get("category") == "Productivity", "marketplace category must be Productivity", errors)

    for rel in REQUIRED_FILES:
        require((ROOT / rel).exists(), f"missing required file: {rel}", errors)

    require(not (ROOT / ".claude").exists(), ".claude directory should not exist in Codex plugin", errors)
    require(not (ROOT / "CLAUDE.md").exists(), "CLAUDE.md should be renamed to AGENTS.md", errors)

    for strategy in (ROOT / "strategies").glob("*.example.md"):
        content = strategy.read_text(encoding="utf-8")
        require("status: paused" in content, f"{strategy.relative_to(ROOT)} must ship paused", errors)

    daily = (ROOT / "commands/investment-daily.md").read_text(encoding="utf-8")
    require("trading-with-confirmation" in daily, "daily command must document trading-with-confirmation mode", errors)
    require("EXECUTE" in daily, "daily command must require exact EXECUTE confirmation", errors)
    require("workspace-bootstrap.py" in daily, "daily command must run workspace bootstrap", errors)

    setup = (ROOT / "commands/investment-setup.md").read_text(encoding="utf-8")
    require("workspace-bootstrap.py" in setup, "setup command must run workspace bootstrap", errors)
    require("proposal-only" in setup, "setup command must configure proposal-only mode", errors)

    nested_commands = list((ROOT / "commands").glob("*/*.md"))
    require(not nested_commands, "commands must be top-level commands/*.md files for Codex plugin command discovery", errors)

    expected_commands = {
        "investment-setup": "commands/investment-setup.md",
        "investment-daily": "commands/investment-daily.md",
        "investment-new-strategy": "commands/investment-new-strategy.md",
        "investment-help": "commands/investment-help.md",
    }
    for command in (ROOT / "commands").glob("*.md"):
        rel = str(command.relative_to(ROOT))
        content = command.read_text(encoding="utf-8")
        require(rel in expected_commands.values(), f"unexpected command file: {rel}", errors)
        require(content.startswith("# /investment-"), f"{rel} should start with a Codex slash-command heading", errors)
    for command_name, rel in expected_commands.items():
        content = (ROOT / rel).read_text(encoding="utf-8")
        require(content.startswith(f"# /{command_name}\n"), f"{rel} should define /{command_name}", errors)

    for skill in (ROOT / "skills").glob("*/SKILL.md"):
        content = skill.read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1] if content.startswith("---\n") else ""
        require(content.startswith("---\n"), f"{skill.relative_to(ROOT)} should start with YAML frontmatter", errors)
        require("name:" in frontmatter, f"{skill.relative_to(ROOT)} needs frontmatter name", errors)
        require("description:" in frontmatter, f"{skill.relative_to(ROOT)} needs frontmatter description", errors)

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
