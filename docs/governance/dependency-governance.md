# bluetape4k Dependency Governance

## Purpose

Dependency updates are handled in two layers:

- Dependabot detects repository-local Gradle and GitHub Actions updates and
  opens reviewable PRs.
- The central version drift report checks whether shared artifacts remain
  consistent across governed repositories.

This split is intentional. Dependabot is repository-scoped, while release
readiness depends on cross-repository consistency.

## Governed Repositories

The governed scope covers the main bluetape4k libraries plus:

- `bluetape4k-workshop`
- `clinic-appointment`
- `exposed-workshop`
- `exposed-r2dbc-workshop`
- `timefold-workshop`

`ocean-workshop` and `kotlin-dev-agent` are intentionally excluded.

## Dependabot Baseline

Each governed repository should define `.github/dependabot.yml` with:

- `gradle` ecosystem for the root build.
- `github-actions` ecosystem for workflow actions.
- `target-branch: develop` for project repositories.
- `target-branch: main` for the central `.github` repository.
- `debop` as the default assignee.
- Grouped updates for Kotlin, Spring, Testcontainers, Jackson, AWS, and
  bluetape4k artifacts when those groups apply.

Invalid placeholder ecosystems such as `dependabot`, `dependency update`, or
misspelled custom values are not valid Dependabot configuration.

## Validation Ladder

| Update type | Validation |
|---|---|
| Local patch/minor dependency | Repository CI. |
| Dependency used by integration tests, containers, serialization, persistence, or runtime adapters | Repository CI plus affected Nightly before merge or explicitly deferred in the PR. |
| Shared baseline dependency such as Kotlin, Spring Boot, Gradle, Testcontainers, Jackson, Exposed, AWS SDK, or Apache Fory | Repository CI plus affected repository Nightly. Run all governed library Nightlies when the affected set is unclear. |
| `bluetape4k-dependencies` BOM | Version drift report plus release/snapshot target Nightlies. |
| Major/runtime/compiler/plugin update | Version drift report, affected Nightly, and manual Weekly Full Nightly before release. |

The point is to avoid discovering breakage days later in a different repository.
Do not merge high-risk updates on repository CI alone.

## Current Drift Notes

Testcontainers and Jackson are expected to stay aligned across governed
repositories.

Apache Fory currently has known drift because its use is concentrated in
serialization-heavy modules and examples. Before the May 2026 release freeze,
either align Fory or keep a linked issue documenting why each exception is
intentional and which Nightly runs covered it.
