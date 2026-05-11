#!/usr/bin/env python3
"""Report security baseline coverage across governed bluetape4k repositories."""
from __future__ import annotations

import argparse
from pathlib import Path


REPOSITORIES = (
    ".github",
    "bluetape4k-aws",
    "bluetape4k-dependencies",
    "bluetape4k-experimental",
    "bluetape4k-exposed",
    "bluetape4k-graph",
    "bluetape4k-image",
    "bluetape4k-javers",
    "bluetape4k-leader",
    "bluetape4k-projects",
    "bluetape4k-text",
    "bluetape4k-workshop",
    "clinic-appointment",
    "exposed-workshop",
    "exposed-r2dbc-workshop",
    "timefold-workshop",
)


def read_workflows(repo: Path) -> str:
    workflow_dir = repo / ".github" / "workflows"
    if not workflow_dir.exists():
        return ""
    return "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in sorted(workflow_dir.glob("*.yml"))
    )


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    args = parser.parse_args()

    root = args.workspace.resolve()
    has_default_security = (root / ".github" / "SECURITY.md").exists()
    rows: list[tuple[str, str, str, str, str, str]] = []

    for name in REPOSITORIES:
        repo = root / name
        workflows = read_workflows(repo)
        has_security = (repo / "SECURITY.md").exists() or has_default_security
        has_dependabot = (repo / ".github" / "dependabot.yml").exists()
        has_gitleaks = "gitleaks" in workflows.lower()
        has_codeql = "github/codeql-action" in workflows
        has_dependency_submission = (
            "dependency-submission" in workflows
            or "submit-gradle" in workflows
            or "dependency-graph" in workflows
        )
        rows.append(
            (
                name,
                yes_no(has_security),
                yes_no(has_dependabot),
                yes_no(has_gitleaks),
                yes_no(has_codeql),
                yes_no(has_dependency_submission),
            )
        )

    print("# bluetape4k Security Baseline Audit")
    print()
    print("| Repository | SECURITY.md/default | Dependabot | Gitleaks | CodeQL | Dependency submission |")
    print("|---|---|---|---|---|---|")
    for row in rows:
        name, *values = row
        print(f"| `{name}` | " + " | ".join(values) + " |")

    missing_critical = [
        name
        for name, security, dependabot, gitleaks, _codeql, _submission in rows
        if security == "no" or dependabot == "no" or gitleaks == "no"
    ]
    print()
    print("## Notes")
    print()
    print("- `SECURITY.md/default` is `yes` for `.github` because it provides the organization default security policy.")
    print("- CodeQL and dependency submission are reported separately because not every governed repository has the same cost/benefit profile.")
    print("- `ocean-workshop` and `kotlin-dev-agent` are intentionally excluded.")
    if missing_critical:
        print("- Repositories missing baseline policy, Dependabot, or gitleaks: " + ", ".join(f"`{name}`" for name in missing_critical) + ".")
    else:
        print("- All governed repositories have security policy coverage, Dependabot, and gitleaks coverage.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
