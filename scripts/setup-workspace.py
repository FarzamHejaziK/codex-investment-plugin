#!/usr/bin/env python3
"""Create or update the local Codex Investment workspace config."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
CONFIG_EXAMPLE = CONFIG_DIR / "workspace.example.json"
CONFIG_PATH = CONFIG_DIR / "workspace.json"
DEFAULT_EXECUTION_MODE = "proposal-only"
EXECUTION_MODES = {"proposal-only", "trading-with-confirmation"}
ALPACA_ACCOUNT_MODES = {"paper", "live"}


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    return value if isinstance(value, dict) else {}


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def ensure_dirs() -> None:
    for rel in ("config", "journal", "strategies", "docs", "skills"):
        (ROOT / rel).mkdir(parents=True, exist_ok=True)
    gitkeep = ROOT / "journal" / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def default_config() -> dict[str, Any]:
    example = load_json(CONFIG_EXAMPLE)
    if not example:
        example = {
            "schema_version": 1,
            "workspace_type": "codex-investment-workspace",
            "execution_mode": DEFAULT_EXECUTION_MODE,
            "alpaca_account_mode": None,
            "created_at": None,
        }
    example["created_at"] = example.get("created_at") or iso_now()
    return example


def update_config(execution_mode: str | None, alpaca_account_mode: str | None) -> dict[str, Any]:
    config = default_config()
    config.update(load_json(CONFIG_PATH))
    config.setdefault("schema_version", 1)
    config["workspace_type"] = "codex-investment-workspace"
    config.setdefault("created_at", iso_now())
    config.setdefault("execution_mode", DEFAULT_EXECUTION_MODE)
    config.setdefault("alpaca_account_mode", None)
    if execution_mode:
        config["execution_mode"] = execution_mode
    if alpaca_account_mode:
        config["alpaca_account_mode"] = alpaca_account_mode
    write_json(CONFIG_PATH, config)
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable workspace details.")
    parser.add_argument("--execution-mode", choices=sorted(EXECUTION_MODES))
    parser.add_argument("--alpaca-account-mode", choices=sorted(ALPACA_ACCOUNT_MODES))
    args = parser.parse_args()

    ensure_dirs()
    config = update_config(args.execution_mode, args.alpaca_account_mode)
    result = {
        "workspace_path": str(ROOT),
        "config_path": str(CONFIG_PATH),
        "execution_mode": config.get("execution_mode", DEFAULT_EXECUTION_MODE),
        "alpaca_account_mode": config.get("alpaca_account_mode"),
        "strategies_path": str(ROOT / "strategies"),
        "journal_path": str(ROOT / "journal"),
    }

    if args.json:
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print(f"Codex Investment workspace: {ROOT}")
        print(f"Config: {CONFIG_PATH}")
        print(f"Execution mode: {result['execution_mode']}")
        print(f"Alpaca account mode: {result['alpaca_account_mode'] or 'not set'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
