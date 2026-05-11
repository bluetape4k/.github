#!/usr/bin/env python3
"""
Report shared dependency version drift across bluetape4k repositories.

The script reads each sibling repository's `gradle/libs.versions.toml` and
prints a Markdown inventory for organization-governed version aliases.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


LIBRARY_REPOSITORIES = (
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
)

WORKSHOP_REPOSITORIES = (
    "bluetape4k-workshop",
    "clinic-appointment",
    "exposed-workshop",
    "exposed-r2dbc-workshop",
    "timefold-workshop",
)

VERSION_GROUPS = {
    "bluetape4k": ("bluetape4k",),
    "bluetape4k dependencies BOM": ("bluetape4k-dependencies",),
    "Kotlin": ("kotlin",),
    "Spring Boot": ("spring-boot", "spring-boot4"),
    "Testcontainers": ("testcontainers",),
    "Jackson 2": ("jackson",),
    "Jackson 3": ("jackson3",),
    "Exposed": ("exposed",),
    "Lettuce": ("lettuce",),
    "Redisson": ("redisson",),
    "AWS Kotlin SDK": ("aws-kotlin",),
    "Smithy Kotlin": ("aws-smithy-kotlin",),
    "Kover": ("kover",),
    "Apache Fory": ("fory", "fory-kotlin"),
}

VERSION_LINE = re.compile(r'^([A-Za-z0-9_.-]+)\s*=\s*"([^"]+)"')
INLINE_VERSION_LINE = re.compile(r'^([A-Za-z0-9_.-]+)\s*=\s*\{.*\bversion\s*=\s*"([^"]+)".*}')


@dataclass(frozen=True)
class VersionHit:
    repo: str
    alias: str
    version: str


def parse_versions(path: Path) -> dict[str, str]:
    versions: dict[str, str] = {}
    in_versions = False

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("[") and stripped.endswith("]"):
            in_versions = stripped == "[versions]"
            continue

        inline_match = INLINE_VERSION_LINE.match(stripped)
        if inline_match:
            versions[inline_match.group(1)] = inline_match.group(2)
            continue

        if in_versions:
            match = VERSION_LINE.match(stripped)
            if match:
                versions[match.group(1)] = match.group(2)

    return versions


def collect(workspace: Path) -> dict[str, list[VersionHit]]:
    grouped: dict[str, list[VersionHit]] = {name: [] for name in VERSION_GROUPS}

    for repo in (*LIBRARY_REPOSITORIES, *WORKSHOP_REPOSITORIES):
        catalog = workspace / repo / "gradle" / "libs.versions.toml"
        if not catalog.exists():
            continue

        versions = parse_versions(catalog)
        for group, aliases in VERSION_GROUPS.items():
            for alias in aliases:
                version = versions.get(alias)
                if version is not None:
                    grouped[group].append(VersionHit(repo, alias, version))

    return grouped


def status_for(hits: list[VersionHit]) -> str:
    if not hits:
        return "missing"
    versions = {hit.version for hit in hits}
    return "aligned" if len(versions) == 1 else "drift"


def render_markdown(grouped: dict[str, list[VersionHit]]) -> tuple[str, bool]:
    lines: list[str] = [
        "# bluetape4k Shared Version Drift Report",
        "",
        "## Scope",
        "",
        "Library repositories: "
        + ", ".join(f"`{repo}`" for repo in LIBRARY_REPOSITORIES)
        + ".",
        "",
        "Workshop/example repositories: "
        + ", ".join(f"`{repo}`" for repo in WORKSHOP_REPOSITORIES)
        + ".",
        "",
        "| Group | Status | Versions | Repositories |",
        "|---|---|---|---|",
    ]

    has_drift = False
    for group, hits in grouped.items():
        status = status_for(hits)
        has_drift = has_drift or status == "drift"

        by_version: dict[str, list[str]] = {}
        for hit in hits:
            by_version.setdefault(hit.version, []).append(f"{hit.repo} (`{hit.alias}`)")

        versions = "<br>".join(
            f"`{version}`: {len(repos)}"
            for version, repos in sorted(by_version.items())
        ) or "-"
        repos = "<br>".join(
            f"`{version}` -> " + ", ".join(sorted(repos))
            for version, repos in sorted(by_version.items())
        ) or "-"

        lines.append(f"| {group} | {status} | {versions} | {repos} |")

    lines.extend(
        [
            "",
            "## Policy Notes",
            "",
            "- `missing` means the repository has no matching alias in its version catalog; it may still use the dependency transitively or not at all.",
            "- `aligned` means all repositories that declare the group use the same version value.",
            "- `drift` means at least two declared values exist and should be resolved or documented before release freeze.",
            "- `ocean-workshop` and `kotlin-dev-agent` are intentionally excluded from this governance scope.",
        ],
    )
    return "\n".join(lines) + "\n", has_drift


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Workspace directory containing bluetape4k-* repositories.",
    )
    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Return exit code 1 when any governed version group has drift.",
    )
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    grouped = collect(workspace)
    markdown, has_drift = render_markdown(grouped)
    sys.stdout.write(markdown)
    return 1 if args.fail_on_drift and has_drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
