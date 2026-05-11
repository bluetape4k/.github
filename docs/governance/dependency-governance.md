# bluetape4k Dependency Governance

## Purpose

Dependency updates are handled in three layers:

- Dependabot detects repository-local Gradle and GitHub Actions updates and
  opens reviewable PRs.
- The central version drift report checks whether shared artifacts remain
  consistent across governed repositories.
- `bluetape4k-projects` is the default baseline for shared runtime libraries
  when it declares the same version alias.

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
- Grouped updates for Kotlin, Spring, Testcontainers, Jackson, Redis clients, AWS, and
  bluetape4k artifacts when those groups apply.

Invalid placeholder ecosystems such as `dependabot`, `dependency update`, or
misspelled custom values are not valid Dependabot configuration.

## Validation Ladder

| Update type | Validation |
|---|---|
| Local patch/minor dependency | Repository CI. |
| Dependency used by integration tests, containers, serialization, persistence, or runtime adapters | Repository CI plus affected Nightly before merge or explicitly deferred in the PR. |
| Shared baseline dependency such as Kotlin, Spring Boot, Gradle, Testcontainers, Jackson, Redis clients, Exposed, AWS SDK, or Apache Fory | Repository CI plus affected repository Nightly. Run all governed library Nightlies when the affected set is unclear. |
| `bluetape4k-dependencies` BOM | Version drift report plus release/snapshot target Nightlies. |
| Major/runtime/compiler/plugin update | Version drift report, affected Nightly, and manual Weekly Full Nightly before release. |

The point is to avoid discovering breakage days later in a different repository.
Do not merge high-risk updates on repository CI alone.

## Current Drift Notes

Testcontainers, Jackson, and Redis client baselines are expected to stay aligned
across governed repositories. For Redis clients such as Lettuce and Redisson,
start major-version adoption in `bluetape4k-projects`, validate the affected
runtime adapters there first, then align the rest of the organization.

Apache Fory currently has known drift because its use is concentrated in
serialization-heavy modules and examples. Before the May 2026 release freeze,
either align Fory or keep a linked issue documenting why each exception is
intentional and which Nightly runs covered it.
