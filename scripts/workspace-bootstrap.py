#!/usr/bin/env python3
"""Create or locate the user's Codex Investment Plugin workspace.

The installed plugin is code. The workspace is user data: strategies, journal
entries, and local configuration. This script keeps those concerns separated.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLUGIN_NAME = "codex-investment-plugin"
PLUGIN_VERSION = "0.1.0"
SOURCE_UPSTREAM = "FarzamHejaziK/claude-investment-assistant"
SOURCE_COMMIT = "9607f6b52214f20e340c1c27491766b78b7acc78"
CONFIG_DIR = Path.home() / ".codex-investment-plugin"
CONFIG_PATH = CONFIG_DIR / "config.json"
MARKER_NAME = ".investment-assistant-workspace.json"
DEFAULT_EXECUTION_MODE = "proposal-only"
EXECUTION_MODES = {"proposal-only", "trading-with-confirmation"}


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def plugin_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_workspace_path() -> Path:
    home = Path.home()
    if platform.system().lower().startswith("win"):
        return home / "Documents" / "codex-investment-plugin-workspace"
    return home / "Documents" / "codex-investment-plugin-workspace"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    tmp.replace(path)


def is_workspace(path: Path) -> bool:
    marker = load_json(path / MARKER_NAME)
    return marker.get("workspace_type") == PLUGIN_NAME


def configured_workspace() -> Path | None:
    cfg = load_json(CONFIG_PATH)
    raw_path = cfg.get("workspace_path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None
    candidate = Path(raw_path).expanduser()
    return candidate if candidate.exists() and candidate.is_dir() else None


def resolve_workspace() -> tuple[Path, str]:
    env_path = os.environ.get("CODEX_INVESTMENT_WORKSPACE")
    if env_path:
        return Path(env_path).expanduser(), "CODEX_INVESTMENT_WORKSPACE"

    cwd = Path.cwd()
    if is_workspace(cwd):
        return cwd, "current directory marker"

    cfg_workspace = configured_workspace()
    if cfg_workspace is not None:
        return cfg_workspace, str(CONFIG_PATH)

    return default_workspace_path(), "default"


def ensure_writable(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    test_path = path / ".write-test"
    try:
        test_path.write_text("ok\n", encoding="utf-8")
        test_path.unlink()
    except OSError as exc:
        raise SystemExit(f"Workspace is not writable: {path} ({exc})") from exc


def seed_workspace(workspace: Path) -> list[str]:
    seeded: list[str] = []
    root = plugin_root()

    strategies_dir = workspace / "strategies"
    strategies_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted((root / "strategies").glob("*.example.md")):
        target = strategies_dir / source.name
        if not target.exists():
            shutil.copy2(source, target)
            seeded.append(str(target.relative_to(workspace)))

    journal_dir = workspace / "journal"
    journal_dir.mkdir(parents=True, exist_ok=True)
    gitkeep = journal_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")
        seeded.append(str(gitkeep.relative_to(workspace)))

    readme = workspace / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Codex Investment Plugin Workspace\n\n"
            "This folder stores your personal investment strategy files and daily journal memos.\n\n"
            "- `strategies/` contains strategy examples and your active strategy files.\n"
            "- `journal/` contains daily memos written by `/investment:daily`.\n"
            "- `.investment-assistant-workspace.json` records local plugin settings.\n\n"
            "Keep this folder private if your strategies, account metadata, or journal entries are sensitive.\n",
            encoding="utf-8",
        )
        seeded.append("README.md")

    return seeded


def update_config(workspace: Path, execution_mode: str | None = None) -> dict[str, Any]:
    cfg = load_json(CONFIG_PATH)
    cfg.setdefault("created_at", iso_now())
    cfg["workspace_path"] = str(workspace)
    cfg["plugin_version"] = PLUGIN_VERSION
    cfg.setdefault("execution_mode", DEFAULT_EXECUTION_MODE)
    if execution_mode:
        cfg["execution_mode"] = execution_mode
    write_json(CONFIG_PATH, cfg)
    return cfg


def update_marker(workspace: Path, config: dict[str, Any]) -> dict[str, Any]:
    marker_path = workspace / MARKER_NAME
    marker = load_json(marker_path)
    marker.setdefault("created_at", iso_now())
    marker.update(
        {
            "schema_version": 1,
            "workspace_type": PLUGIN_NAME,
            "created_by": PLUGIN_NAME,
            "source_upstream": SOURCE_UPSTREAM,
            "source_commit": SOURCE_COMMIT,
            "plugin_version": PLUGIN_VERSION,
            "execution_mode": config.get("execution_mode", DEFAULT_EXECUTION_MODE),
        }
    )
    write_json(marker_path, marker)
    return marker


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable workspace details.")
    parser.add_argument(
        "--execution-mode",
        choices=sorted(EXECUTION_MODES),
        help="Persist the default execution mode for future runs.",
    )
    args = parser.parse_args()

    workspace, source = resolve_workspace()
    workspace = workspace.expanduser().resolve()
    ensure_writable(workspace)
    seeded = seed_workspace(workspace)
    config = update_config(workspace, args.execution_mode)
    marker = update_marker(workspace, config)

    result = {
        "workspace_path": str(workspace),
        "resolution_source": source,
        "config_path": str(CONFIG_PATH),
        "marker_path": str(workspace / MARKER_NAME),
        "execution_mode": marker.get("execution_mode", DEFAULT_EXECUTION_MODE),
        "seeded": seeded,
    }

    if args.json:
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print(f"Codex Investment Plugin workspace: {workspace}")
        print(f"Resolution source: {source}")
        print(f"Execution mode: {result['execution_mode']}")
        if seeded:
            print("Seeded: " + ", ".join(seeded))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
