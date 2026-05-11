#!/usr/bin/env python3
"""Check or sync bluetape4k workspace-root guidance documents."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


WORKSPACE_DOCS = ("AGENTS.md", "CLAUDE.md", "WIP.md")


def default_paths() -> tuple[Path, Path]:
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root, repo_root.parent


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def check_or_sync(source_dir: Path, workspace: Path, sync: bool) -> int:
    missing: list[str] = []
    drifted: list[str] = []

    for name in WORKSPACE_DOCS:
        source = source_dir / name
        target = workspace / name

        if not source.exists():
            missing.append(f"missing canonical source: {source}")
            continue

        if not target.exists():
            if sync:
                copy_file(source, target)
                print(f"created {target}")
            else:
                missing.append(f"missing workspace target: {target}")
            continue

        if not filecmp.cmp(source, target, shallow=False):
            if sync:
                copy_file(source, target)
                print(f"updated {target}")
            else:
                drifted.append(name)

    if missing:
        print("\n".join(missing), file=sys.stderr)
    if drifted:
        print("workspace docs drifted: " + ", ".join(drifted), file=sys.stderr)

    return 1 if missing or drifted else 0


def parse_args() -> argparse.Namespace:
    repo_root, workspace = default_paths()
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail when workspace docs drift")
    mode.add_argument("--sync", action="store_true", help="copy canonical docs to workspace root")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=repo_root / "docs" / "workspace",
        help="canonical workspace docs directory",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=workspace,
        help="workspace root containing active AGENTS.md, CLAUDE.md, and WIP.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return check_or_sync(
        source_dir=args.source_dir.resolve(),
        workspace=args.workspace.resolve(),
        sync=args.sync,
    )


if __name__ == "__main__":
    raise SystemExit(main())
