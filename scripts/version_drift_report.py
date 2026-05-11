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

BASELINE_REPOSITORY = "bluetape4k-projects"

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
    "Spring Boot": ("spring-boot",),
    "Spring Boot 3": ("spring-boot3",),
    "Spring Boot 4": ("spring-boot4",),
    "Kafka 3": ("kafka3",),
    "Kafka 4": ("kafka4",),
    "Spring Kafka 3": ("spring-kafka",),
    "Spring Kafka 4": ("spring-kafka4",),
    "Testcontainers": ("testcontainers",),
    "Jackson 2": ("jackson",),
    "Jackson 3": ("jackson3",),
    "Exposed": ("exposed",),
    "Apache Ignite 2": ("ignite",),
    "Apache Ignite 3": ("ignite3",),
    "Lettuce": ("lettuce",),
    "Redisson": ("redisson",),
    "AWS Kotlin SDK": ("aws-kotlin",),
    "Smithy Kotlin": ("aws-smithy-kotlin",),
    "Kover": ("kover",),
    "Apache Fory": ("fory", "fory-kotlin"),
}

COMPATIBILITY_LINE_ALIASES = {
    "ignite3": "3",
    "jackson2": "2",
    "jackson3": "3",
    "kafka3": "3",
    "kafka4": "4",
    "spring-boot3": "3",
    "spring-boot4": "4",
    "spring-kafka3": "3",
    "spring-kafka4": "4",
}

PAIRED_LEGACY_LINE_ALIASES = {
    "ignite": ("ignite3", "2"),
    "jackson": ("jackson3", "2"),
    "spring-kafka": ("spring-kafka4", "3"),
}

VERSION_MAJOR = re.compile(r"^(\d+)")

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


def collect_repository_versions(workspace: Path, repositories: tuple[str, ...]) -> dict[str, dict[str, str]]:
    repo_versions: dict[str, dict[str, str]] = {}
    for repo in repositories:
        catalog = workspace / repo / "gradle" / "libs.versions.toml"
        if catalog.exists():
            repo_versions[repo] = parse_versions(catalog)
    return repo_versions


def collect_shared_alias_drift(workspace: Path) -> dict[str, list[VersionHit]]:
    repo_versions = collect_repository_versions(workspace, LIBRARY_REPOSITORIES)
    manual_aliases = {alias for aliases in VERSION_GROUPS.values() for alias in aliases}

    aliases: dict[str, list[VersionHit]] = {}
    for repo, versions in repo_versions.items():
        for alias, version in versions.items():
            if alias in manual_aliases:
                continue
            aliases.setdefault(alias, []).append(VersionHit(repo, alias, version))

    return {
        alias: hits
        for alias, hits in sorted(aliases.items())
        if len({hit.repo for hit in hits}) >= 2 and status_for(hits) == "drift"
    }


def collect_compatibility_line_violations(workspace: Path) -> list[VersionHit]:
    repo_versions = collect_repository_versions(workspace, (*LIBRARY_REPOSITORIES, *WORKSHOP_REPOSITORIES))
    violations: list[VersionHit] = []

    for repo, versions in repo_versions.items():
        for alias, expected_major in COMPATIBILITY_LINE_ALIASES.items():
            version = versions.get(alias)
            if version is None:
                continue

            major_match = VERSION_MAJOR.match(version)
            if major_match is None or major_match.group(1) != expected_major:
                violations.append(VersionHit(repo, alias, version))

        for alias, (paired_alias, expected_major) in PAIRED_LEGACY_LINE_ALIASES.items():
            version = versions.get(alias)
            if version is None or paired_alias not in versions:
                continue

            major_match = VERSION_MAJOR.match(version)
            if major_match is None or major_match.group(1) != expected_major:
                violations.append(VersionHit(repo, alias, version))

    return violations


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


def render_shared_alias_drift(shared_alias_drift: dict[str, list[VersionHit]]) -> tuple[str, bool]:
    lines: list[str] = [
        "",
        "## Auto-Discovered Shared Alias Drift",
        "",
        "`bluetape4k-*` library repositories are scanned for version aliases declared by at least two repositories.",
        f"When `{BASELINE_REPOSITORY}` declares the same alias, its value is the default baseline.",
        "",
        "| Alias | Baseline | Versions | Repositories |",
        "|---|---|---|---|",
    ]

    if not shared_alias_drift:
        lines.append("| - | - | - | No drift among shared library aliases. |")
        return "\n".join(lines) + "\n", False

    for alias, hits in shared_alias_drift.items():
        by_version: dict[str, list[str]] = {}
        baseline = "-"
        for hit in hits:
            by_version.setdefault(hit.version, []).append(hit.repo)
            if hit.repo == BASELINE_REPOSITORY:
                baseline = hit.version

        versions = "<br>".join(
            f"`{version}`: {len(repos)}"
            for version, repos in sorted(by_version.items())
        )
        repos = "<br>".join(
            f"`{version}` -> " + ", ".join(f"`{repo}`" for repo in sorted(repos))
            for version, repos in sorted(by_version.items())
        )
        lines.append(f"| `{alias}` | `{baseline}` | {versions} | {repos} |")

    return "\n".join(lines) + "\n", True


def render_compatibility_line_violations(violations: list[VersionHit]) -> tuple[str, bool]:
    lines: list[str] = [
        "",
        "## Compatibility-Line Alias Violations",
        "",
        "These aliases encode product or platform compatibility lines. Dependabot may see the same Maven coordinates and propose a newer major, but these aliases must stay on their declared line unless the alias itself changes.",
        "",
        "| Repository | Alias | Expected major | Actual version |",
        "|---|---|---|---|",
    ]

    if not violations:
        lines.append("| - | - | - | No compatibility-line alias violations. |")
        return "\n".join(lines) + "\n", False

    for hit in sorted(violations, key=lambda item: (item.repo, item.alias)):
        if hit.alias in COMPATIBILITY_LINE_ALIASES:
            expected_major = COMPATIBILITY_LINE_ALIASES[hit.alias]
        else:
            expected_major = PAIRED_LEGACY_LINE_ALIASES[hit.alias][1]
        lines.append(f"| `{hit.repo}` | `{hit.alias}` | `{expected_major}.x` | `{hit.version}` |")

    return "\n".join(lines) + "\n", True


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
    shared_markdown, has_shared_alias_drift = render_shared_alias_drift(collect_shared_alias_drift(workspace))
    compatibility_markdown, has_compatibility_violations = render_compatibility_line_violations(
        collect_compatibility_line_violations(workspace),
    )
    sys.stdout.write(markdown)
    sys.stdout.write(shared_markdown)
    sys.stdout.write(compatibility_markdown)
    has_drift = has_drift or has_shared_alias_drift or has_compatibility_violations
    return 1 if args.fail_on_drift and has_drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
