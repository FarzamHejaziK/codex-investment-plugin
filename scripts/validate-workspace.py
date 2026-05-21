#!/usr/bin/env python3
"""Validate the Codex Investment workspace repository shape."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
    ".docs/plan.md",
    "config/workspace.example.json",
    "journal/.gitkeep",
    "scripts/setup-workspace.py",
    "scripts/alpaca-mcp-wrapper.sh",
    "scripts/validate-workspace.py",
    "skills/setup/SKILL.md",
    "skills/daily/SKILL.md",
    "skills/new-strategy/SKILL.md",
    "skills/help/SKILL.md",
    "strategies/dip-buying.example.md",
    "strategies/ai-value-chain.example.md",
    "strategies/active-trading.example.md",
    "docs/getting-started.md",
    "docs/workspace.md",
    "docs/alpaca-setup.md",
    "docs/designing-a-strategy.md",
    "docs/faq.md",
    "docs/safety-and-limits.md",
    "docs/trading-mode.md",
]

REMOVED_FILES = [
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "scripts/workspace-bootstrap.py",
    "scripts/validate-plugin.py",
]

FORBIDDEN_PATTERNS = [
    (re.compile(r"\bclaude mcp\b", re.IGNORECASE), "Claude MCP command"),
    (re.compile(r"\.claude/"), ".claude runtime path"),
    (re.compile(r"Claude Code"), "Claude Code product reference"),
    (re.compile(r"codex plugin marketplace add"), "plugin marketplace install command"),
    (re.compile(r"/plugins\b"), "plugin browser instruction"),
    (re.compile(r"/investment-(setup|daily|new-strategy|help)"), "old slash-command instruction"),
    (re.compile(r"workspace-bootstrap\.py"), "old bootstrap script name"),
    (re.compile(r"validate-plugin\.py"), "old validation script name"),
]

FORBIDDEN_SKIP = {
    ".docs/plan.md",
    "CHANGELOG.md",
    "scripts/validate-workspace.py",
}

SECRET_PATTERNS = [
    re.compile(r"ALPACA_SECRET_KEY\s*=\s*['\"](?!\$\()[^'\"\s]{12,}['\"]"),
    re.compile(r"ALPACA_API_KEY\s*=\s*['\"](?!\$\()[^'\"\s]{12,}['\"]"),
    re.compile(r"\b(SK|PK|AK)[A-Z0-9]{12,}\b"),
]


def text_files() -> list[Path]:
    ignored = {".git", "docs/assets"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if not path.is_file() or any(str(rel).startswith(part) for part in ignored):
            continue
        if path.suffix.lower() in {".md", ".json", ".py", ".sh", ".txt", ".toml"} or path.name == ".gitignore":
            files.append(path)
    return files


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        require((ROOT / rel).exists(), f"missing required file: {rel}", errors)

    for rel in REMOVED_FILES:
        require(not (ROOT / rel).exists(), f"removed plugin-era file still exists: {rel}", errors)

    require(not (ROOT / "commands").exists(), "commands/ should be removed; workflows live in skills/", errors)

    try:
        config = json.loads((ROOT / "config/workspace.example.json").read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"config/workspace.example.json is invalid: {exc}")
        config = {}
    require(config.get("workspace_type") == "codex-investment-workspace", "workspace example has wrong type", errors)
    require(config.get("execution_mode") == "proposal-only", "workspace example must default proposal-only", errors)

    expected_skills = {"setup", "daily", "new-strategy", "help"}
    skill_dirs = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    require(skill_dirs == expected_skills, f"skills must be exactly {sorted(expected_skills)}", errors)
    for name in expected_skills:
        skill_path = ROOT / "skills" / name / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8") if skill_path.exists() else ""
        frontmatter = content.split("---", 2)[1] if content.startswith("---\n") else ""
        require(content.startswith("---\n"), f"{skill_path.relative_to(ROOT)} needs frontmatter", errors)
        require(f'name: "{name}"' in frontmatter, f"{skill_path.relative_to(ROOT)} name must be {name}", errors)
        require("description:" in frontmatter, f"{skill_path.relative_to(ROOT)} needs description", errors)

    for strategy in (ROOT / "strategies").glob("*.example.md"):
        content = strategy.read_text(encoding="utf-8")
        require("status: paused" in content, f"{strategy.relative_to(ROOT)} must ship paused", errors)

    for path in text_files():
        rel = str(path.relative_to(ROOT))
        if rel in FORBIDDEN_SKIP:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for pattern, label in FORBIDDEN_PATTERNS:
            if pattern.search(content):
                errors.append(f"{rel} contains forbidden {label}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"{rel} appears to contain a secret-looking value")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
