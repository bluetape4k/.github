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

`scripts/version_drift_report.py` has two scopes:

- Curated release-train groups for dependencies that are known release gates.
- Auto-discovered shared aliases across `bluetape4k-*` library repositories.
  Any alias declared by at least two library repositories is checked for drift,
  and `bluetape4k-projects` is shown as the default baseline when present.
- Compatibility-line aliases such as `ignite`/`ignite3`, `kafka3`/`kafka4`,
  `spring-kafka`/`spring-kafka4`, `jackson`/`jackson3`, and
  `spring-boot`/`spring-boot4`. These aliases must stay on their encoded major
  line even when the Maven coordinates look upgrade-compatible to Dependabot.

## Governed Repositories

The governed scope covers the main bluetape4k libraries plus:

- `bluetape4k-workshop`
- `clinic-appointment`
- `exposed-workshop`
- `exposed-r2dbc-workshop`
- `timefold-workshop`

`ocean-workshop` and `kotlin-dev-agent` are intentionally excluded.

## Workshop and Application Consumers

Workshop, example, and application repositories consume bluetape4k releases;
they do not own independent bluetape4k ecosystem versions. These repositories
should keep `bluetape4k-dependencies` as the only bluetape4k version source in
`gradle/libs.versions.toml`:

- `bluetape4k-workshop`
- `clinic-appointment`
- `exposed-workshop`
- `exposed-r2dbc-workshop`
- `timefold-workshop`

Required catalog shape:

- Define one `bluetape4k-dependencies = "<version>"` version alias.
- Define one library alias for
  `io.github.bluetape4k:bluetape4k-dependencies`.
- Import that BOM through dependency management or Gradle platform
  configuration.
- Declare `io.github.bluetape4k*` artifacts without versions, including core,
  exposed, leader, assertions, and test helper artifacts.

Do not keep consumer-side aliases such as `bluetape4k`, `bluetape4k-bom`,
`bluetape4k-leader`, `bluetape4k-assertions-version`, or
`version.ref = "bluetape4k"` for bluetape4k artifacts. If a historical accessor
name must remain for compatibility, keep the accessor name but point it at the
current BOM-managed artifact and omit the version.

Release-upgrade PRs for these repositories should verify that
`bluetape4k-dependencies` is the only bluetape4k version source, grep for
forbidden direct bluetape4k version references, and compile changed examples or
the full repository when practical.

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
| Compatibility-line alias update such as `ignite`, `ignite3`, `kafka3`, `kafka4`, `spring-kafka`, or `spring-kafka4` | Treat as a platform-line change. Reject PRs that move the alias to a different major; create or update the correct alias instead. |
| `bluetape4k-dependencies` BOM | Version drift report plus release/snapshot target Nightlies. |
| Major/runtime/compiler/plugin update | Version drift report, affected Nightly, and manual Weekly Full Nightly before release. |

The point is to avoid discovering breakage days later in a different repository.
Do not merge high-risk updates on repository CI alone.

## Current Drift Notes

Testcontainers, Jackson, and Redis client baselines are expected to stay aligned
across governed repositories. For Redis clients such as Lettuce and Redisson,
start major-version adoption in `bluetape4k-projects`, validate the affected
runtime adapters there first, then align the rest of the organization.

Compatibility-line aliases are not interchangeable. `ignite` means Apache
Ignite 2.x, while `ignite3` means Apache Ignite 3.x. `spring-kafka` means the
3.x line, while `spring-kafka4` means the 4.x line. Do not merge Dependabot PRs
that rewrite the older alias to the newer major.

Apache Fory currently has known drift because its use is concentrated in
serialization-heavy modules and examples. Before the May 2026 release freeze,
either align Fory or keep a linked issue documenting why each exception is
intentional and which Nightly runs covered it.
