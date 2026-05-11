#!/usr/bin/env python3
"""Audit repository governance inventory and expected workflow files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def workflow_exists(repo: Path, workflow: str) -> bool:
    return (repo / ".github" / "workflows" / workflow).exists()


def repo_configured_for(config: dict[str, Any], repo: str, kind: str) -> str:
    repo_workflows = config.get("repositories", {}).get(repo, {})
    workflow = repo_workflows.get(kind, {}).get("workflow")
    return workflow or "-"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("org-workflows.json"))
    parser.add_argument("--workspace", type=Path, default=Path(".."))
    parser.add_argument("--fail-on-drift", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    workspace = args.workspace.resolve()
    central_security = (workspace / ".github" / "SECURITY.md").exists()
    rows: list[dict[str, str]] = []
    drift = False

    for repo, governance in config["governance"].items():
        repo_path = workspace / repo
        repo_workflows = config.get("repositories", {}).get(repo, {})
        expected_workflows: list[str] = [
            workflow["workflow"]
            for key in ("nightly", "snapshot", "release")
            if (workflow := repo_workflows.get(key))
        ]

        missing_workflows = [
            workflow for workflow in expected_workflows if not workflow_exists(repo_path, workflow)
        ]
        has_dependabot = (repo_path / ".github" / "dependabot.yml").exists()
        has_security = (repo_path / "SECURITY.md").exists() or central_security
        has_security_workflow = any(
            token in "\n".join(
                path.read_text(encoding="utf-8", errors="ignore")
                for path in sorted((repo_path / ".github" / "workflows").glob("*.yml"))
            ).lower()
            for token in ("gitleaks", "codeql")
        ) if (repo_path / ".github" / "workflows").exists() else False
        coverage_policy = governance.get("coverage", "excluded")
        has_coverage_policy = (
            coverage_policy in {"excluded", "report-only"}
            or (repo_path / "docs" / "governance" / "kover-coverage-policy.md").exists()
        )

        repo_drift = bool(missing_workflows)
        repo_drift = repo_drift or (governance.get("dependabot") and not has_dependabot)
        repo_drift = repo_drift or (governance.get("security") and not has_security)
        repo_drift = repo_drift or (governance.get("security") and not has_security_workflow)
        repo_drift = repo_drift or not has_coverage_policy
        drift = drift or repo_drift

        rows.append(
            {
                "repo": repo,
                "dependabot": yes_no(has_dependabot),
                "security_policy": yes_no(has_security),
                "security_workflow": yes_no(has_security_workflow),
                "coverage_policy": coverage_policy if has_coverage_policy else f"missing:{coverage_policy}",
                "nightly": repo_configured_for(config, repo, "nightly"),
                "snapshot": repo_configured_for(config, repo, "snapshot"),
                "release": repo_configured_for(config, repo, "release"),
                "missing_workflows": ", ".join(missing_workflows) or "-",
                "status": "drift" if repo_drift else "ok",
            },
        )

    print("# bluetape4k Workflow and Governance Drift Audit")
    print()
    print("| Repository | Status | Dependabot | Security policy | Security workflow | Coverage | Nightly | Snapshot | Release | Missing workflows |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for row in rows:
        print(
            f"| `{row['repo']}` | {row['status']} | {row['dependabot']} | "
            f"{row['security_policy']} | {row['security_workflow']} | {row['coverage_policy']} | "
            f"`{row['nightly']}` | `{row['snapshot']}` | `{row['release']}` | {row['missing_workflows']} |",
        )

    excluded = config.get("excluded_repositories", {})
    if excluded:
        print()
        print("## Excluded Repositories")
        print()
        for repo, reason in excluded.items():
            print(f"- `{repo}`: {reason}")

    return 1 if drift and args.fail_on_drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
