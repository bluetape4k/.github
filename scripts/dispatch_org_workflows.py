#!/usr/bin/env python3
"""
Dispatch bluetape4k repository workflows from the organization profile repo.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TERMINAL_FAILURES = {"failure", "cancelled", "timed_out", "action_required", "startup_failure"}


@dataclass(frozen=True)
class DispatchTarget:
    repo: str
    workflow: str
    ref: str
    inputs: dict[str, str]


@dataclass
class RunState:
    target: DispatchTarget
    run_id: int | None = None
    html_url: str | None = None
    status: str = "queued"
    conclusion: str | None = None


class GitHubClient:
    def __init__(self, token: str, owner: str) -> None:
        self.token = token
        self.owner = owner

    def request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            f"https://api.github.com{path}",
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status == 204:
                    return None
                payload = response.read()
                return json.loads(payload.decode("utf-8")) if payload else None
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API {method} {path} failed: {error.code} {detail}") from error

    def dispatch(self, target: DispatchTarget) -> None:
        workflow = urllib.parse.quote(target.workflow, safe="")
        self.request(
            "POST",
            f"/repos/{self.owner}/{target.repo}/actions/workflows/{workflow}/dispatches",
            {"ref": target.ref, "inputs": target.inputs},
        )

    def latest_dispatch_run(self, target: DispatchTarget, started_at: dt.datetime) -> RunState | None:
        workflow = urllib.parse.quote(target.workflow, safe="")
        query = urllib.parse.urlencode(
            {
                "event": "workflow_dispatch",
                "branch": target.ref,
                "per_page": "20",
            },
        )
        payload = self.request(
            "GET",
            f"/repos/{self.owner}/{target.repo}/actions/workflows/{workflow}/runs?{query}",
        )
        for run in payload.get("workflow_runs", []):
            created_at = dt.datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
            if created_at >= started_at - dt.timedelta(seconds=10):
                return RunState(
                    target=target,
                    run_id=run["id"],
                    html_url=run["html_url"],
                    status=run["status"],
                    conclusion=run["conclusion"],
                )
        return None

    def run_state(self, state: RunState) -> RunState:
        if state.run_id is None:
            return state
        payload = self.request(
            "GET",
            f"/repos/{self.owner}/{state.target.repo}/actions/runs/{state.run_id}",
        )
        state.status = payload["status"]
        state.conclusion = payload["conclusion"]
        state.html_url = payload["html_url"]
        return state


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def selected_repositories(config: dict[str, Any], kind: str, repositories: str) -> list[str]:
    if repositories == "all":
        return list(config["trains"][kind])

    requested = [repo.strip() for repo in repositories.split(",") if repo.strip()]
    unknown = [repo for repo in requested if repo not in config["repositories"]]
    if unknown:
        raise ValueError(f"Unknown repository name(s): {', '.join(unknown)}")
    return requested


def render_inputs(template: dict[str, str] | None, values: dict[str, str]) -> dict[str, str]:
    if not template:
        return {}
    return {key: raw.format(**values) for key, raw in template.items()}


def build_targets(args: argparse.Namespace, config: dict[str, Any]) -> list[DispatchTarget]:
    values = {
        "scope": args.scope,
        "version": args.version or "",
        "diagnose_signing": bool_text(args.diagnose_signing),
    }
    repos = selected_repositories(config, args.kind, args.repositories)
    targets: list[DispatchTarget] = []

    for repo in repos:
        repo_config = config["repositories"][repo]
        workflow_config = repo_config.get(args.kind)
        if workflow_config is None:
            print(f"Skipping {repo}: no {args.kind} workflow configured", file=sys.stderr)
            continue

        targets.append(
            DispatchTarget(
                repo=repo,
                workflow=workflow_config["workflow"],
                ref=args.ref or repo_config.get("default_ref", "develop"),
                inputs=render_inputs(workflow_config.get("inputs"), values),
            ),
        )

    return targets


def print_plan(targets: list[DispatchTarget]) -> None:
    print("| Repository | Workflow | Ref | Inputs |")
    print("|---|---|---|---|")
    for target in targets:
        inputs = ", ".join(f"`{k}={v}`" for k, v in target.inputs.items()) or "-"
        print(f"| `{target.repo}` | `{target.workflow}` | `{target.ref}` | {inputs} |")


def wait_for_run(client: GitHubClient, target: DispatchTarget, started_at: dt.datetime) -> RunState:
    state: RunState | None = None
    for _ in range(60):
        state = client.latest_dispatch_run(target, started_at)
        if state is not None:
            break
        time.sleep(5)
    if state is None:
        raise RuntimeError(f"Could not find dispatched run for {target.repo}/{target.workflow}")

    while state.status != "completed":
        print(f"{target.repo}: {state.status} {state.html_url or ''}")
        time.sleep(20)
        state = client.run_state(state)

    print(f"{target.repo}: completed conclusion={state.conclusion} {state.html_url or ''}")
    return state


def write_summary(kind: str, dry_run: bool, states: list[RunState], targets: list[DispatchTarget]) -> None:
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary:
        return

    lines = [f"## bluetape4k org {kind} dispatch", ""]
    if dry_run:
        lines.append("_Dry run only. No workflow was dispatched._")
        lines.append("")
        lines.append("| Repository | Workflow | Ref | Inputs |")
        lines.append("|---|---|---|---|")
        for target in targets:
            inputs = ", ".join(f"`{k}={v}`" for k, v in target.inputs.items()) or "-"
            lines.append(f"| `{target.repo}` | `{target.workflow}` | `{target.ref}` | {inputs} |")
    else:
        lines.append("| Repository | Workflow | Status | Conclusion | Run |")
        lines.append("|---|---|---|---|---|")
        for state in states:
            url = state.html_url or ""
            run = f"[run]({url})" if url else "-"
            lines.append(
                f"| `{state.target.repo}` | `{state.target.workflow}` | {state.status} | {state.conclusion or '-'} | {run} |",
            )

    with open(summary, "a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=("nightly", "snapshot", "release"), required=True)
    parser.add_argument("--config", type=Path, default=Path("org-workflows.json"))
    parser.add_argument("--repositories", default="all", help="`all` or comma-separated repository names.")
    parser.add_argument("--ref", default="", help="Override dispatch ref for every target.")
    parser.add_argument("--scope", default="full", help="Nightly scope passed to repositories that support it.")
    parser.add_argument("--version", default="", help="Release version passed to release workflows.")
    parser.add_argument("--diagnose-signing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--wait", action="store_true")
    parser.add_argument("--serial", action="store_true", help="Wait for each target before dispatching the next.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.kind == "release" and not args.version:
        raise SystemExit("--version is required for release dispatch")

    config = load_config(args.config)
    targets = build_targets(args, config)
    if not targets:
        raise SystemExit("No dispatch targets selected")

    print_plan(targets)
    if args.dry_run:
        write_summary(args.kind, True, [], targets)
        return 0

    token = os.environ.get("ORG_WORKFLOW_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("ORG_WORKFLOW_TOKEN, GH_TOKEN, or GITHUB_TOKEN is required for dispatch")

    client = GitHubClient(token=token, owner=config["owner"])
    states: list[RunState] = []
    failed = False

    if args.serial:
        for target in targets:
            started_at = dt.datetime.now(dt.timezone.utc)
            client.dispatch(target)
            state = wait_for_run(client, target, started_at) if args.wait else RunState(target=target)
            states.append(state)
            failed = failed or state.conclusion in TERMINAL_FAILURES
            if failed:
                break
    else:
        started_at = dt.datetime.now(dt.timezone.utc)
        for target in targets:
            client.dispatch(target)
            states.append(RunState(target=target))
        if args.wait:
            states = [wait_for_run(client, target, started_at) for target in targets]
            failed = any(state.conclusion in TERMINAL_FAILURES for state in states)

    write_summary(args.kind, False, states, targets)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
