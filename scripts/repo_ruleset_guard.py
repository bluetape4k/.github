#!/usr/bin/env python3
"""
Audit or apply the bluetape4k default branch protection ruleset.

Organization rulesets require GitHub Team/Enterprise. This script applies the
same repository-level ruleset across governed repositories when org-level
rulesets are unavailable.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys


OWNER = "bluetape4k"
RULESET_NAME = "bluetape4k default branch guard"

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


def ruleset_payload() -> dict:
    return {
        "name": RULESET_NAME,
        "target": "branch",
        "enforcement": "active",
        "conditions": {
            "ref_name": {
                "include": ["~DEFAULT_BRANCH", "refs/heads/main"],
                "exclude": [],
            },
        },
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {
                "type": "pull_request",
                "parameters": {
                    "required_approving_review_count": 0,
                    "dismiss_stale_reviews_on_push": False,
                    "require_code_owner_review": False,
                    "require_last_push_approval": False,
                    "required_review_thread_resolution": False,
                    "allowed_merge_methods": ["merge", "squash", "rebase"],
                },
            },
        ],
    }


def gh_json(path: str, *args: str, input_json: dict | None = None) -> object:
    cmd = ["gh", "api", path, *args]
    data = None
    if input_json is not None:
        data = json.dumps(input_json).encode()
        cmd.extend(["--input", "-"])
    result = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode().strip())
    if not result.stdout:
        return None
    return json.loads(result.stdout)


def find_ruleset(repo: str) -> dict | None:
    rulesets = gh_json(f"/repos/{OWNER}/{repo}/rulesets")
    for ruleset in rulesets:
        if ruleset.get("name") == RULESET_NAME:
            return ruleset
    return None


def apply_ruleset(repo: str, dry_run: bool) -> str:
    existing = find_ruleset(repo)
    payload = ruleset_payload()
    if dry_run:
        return "present" if existing else "missing"

    if existing:
        gh_json(
            f"/repos/{OWNER}/{repo}/rulesets/{existing['id']}",
            "--method",
            "PUT",
            input_json=payload,
        )
        return "updated"

    gh_json(f"/repos/{OWNER}/{repo}/rulesets", "--method", "POST", input_json=payload)
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create or update repository rulesets. Without this flag the script audits only.",
    )
    args = parser.parse_args()

    print("| Repository | Status |")
    print("|---|---|")
    failures = 0
    for repo in REPOSITORIES:
        try:
            status = apply_ruleset(repo, dry_run=not args.apply)
        except Exception as exc:
            failures += 1
            status = f"error: {exc}"
        print(f"| `{repo}` | {status} |")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
