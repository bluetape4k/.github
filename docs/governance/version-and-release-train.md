# bluetape4k Version Governance and Release Train

## Purpose

This document supports the planned official release at the end of May 2026.
It defines the central operating surface for shared dependency drift checks,
organization-wide Nightly dispatch, snapshot publishing, and release train
dispatch.

Dependency update ownership and validation tiers are defined in
`docs/governance/dependency-governance.md`.

## Token Requirement

Cross-repository workflow dispatch requires an organization-scoped token. The
central `.github` repository must define `ORG_WORKFLOW_TOKEN` as a repository or
organization secret.

Recommended token shape:

- GitHub App installation token or fine-grained PAT.
- Repository access: all bluetape4k repositories managed by the train.
- Permissions:
  - Actions: read and write.
  - Contents: read.
  - Metadata: read.

The central workflows only dispatch existing repository workflows. Publishing
credentials, signing keys, and package permissions remain in each target
repository.

## Central Workflows

| Workflow | Purpose | Default safety |
|---|---|---|
| `Org Version Drift` | Clone bluetape4k repos and generate shared version drift report. | Weekly report; optional fail-on-drift. |
| `Org Nightly Dispatch` | Trigger Nightly workflows across selected repositories. | Manual only; `dryRun=true` by default. |
| `Org Snapshot Dispatch` | Trigger snapshot publishing workflows in train order. | Manual only; `dryRun=true`; confirmation phrase required for real dispatch. |
| `Org Release Train` | Trigger release workflows in train order. | Manual only; `dryRun=true`; confirmation phrase required for real dispatch. |

## Train Order

Snapshot dispatch uses this default order:

1. `bluetape4k-projects`
2. `bluetape4k-exposed`
3. `bluetape4k-text`
4. `bluetape4k-graph`
5. `bluetape4k-javers`
6. `bluetape4k-aws`
7. `bluetape4k-leader`
8. `bluetape4k-image`
9. `bluetape4k-dependencies`

`bluetape4k-dependencies` is last because it is the ecosystem BOM and should be
published after the libraries it coordinates. The Gradle build catalog is not
the final BOM and is not a Maven Central publication. Cut an immutable
`bluetape4k-dependencies` git ref such as `catalog/2026-05-23-00` when
repositories in the train need updated external dependency aliases or plugin
versions before the final BOM can exist.

Release dispatch uses the same order, including `bluetape4k-dependencies` as
the final BOM publication. `bluetape4k-experimental` and `bluetape4k-workshop`
are Nightly-only by default.

## Version Management Policy

Use this section as the canonical rule set for `bluetape4k-*` workspace version
management. Release runbooks and checklists are execution surfaces for these
rules.

### Repository Artifact Version

- Every publishable repository keeps its own version in `gradle.properties`:
  `baseVersion=<next release version>` and `snapshotVersion=`.
- After a repository release is complete, immediately advance `baseVersion` on
  `develop` to the next release version. Example: after publishing `0.2.1`,
  set `baseVersion=0.2.2`.
- Keep `snapshotVersion=` empty in git. Do not check `-SNAPSHOT` into
  `gradle.properties` to mark development state.
- Snapshot artifacts are produced only by workflow or command input:
  `-PsnapshotVersion=-SNAPSHOT`.
- Release artifacts are produced from `baseVersion` only. Release workflows must
  fail if `snapshotVersion` is non-empty or if they inject `-SNAPSHOT`.

State table:

| State | `baseVersion` | `snapshotVersion` | Published artifact version |
|---|---|---|---|
| Normal development after release | next release version | empty | none from git alone |
| Snapshot workflow | next release version | injected as `-SNAPSHOT` | `<baseVersion>-SNAPSHOT` |
| Release prep and tag | release version | empty | `<baseVersion>` |
| Maintenance branch | next patch on that line | empty | `<baseVersion>` or `<baseVersion>-SNAPSHOT` only when workflow injects it |

### Internal bluetape4k References

- During ordinary development, a repository that depends on another
  `bluetape4k-*` artifact uses the matching upstream `-SNAPSHOT` version.
  Example: while `bluetape4k-projects` is developing `1.9.2`, downstream
  libraries reference `bluetape4k-bom = 1.9.2-SNAPSHOT` or the equivalent local
  version key.
- During release preparation, remove `-SNAPSHOT` from an internal
  `bluetape4k-*` reference only after that upstream repository has been released
  and the target artifact returns HTTP 200 from Maven Central.
- Do not fall back to the previous public release just because the intended
  upstream release is not visible yet. Wait for the upstream release, or stay on
  the matching upstream snapshot on the development branch.
- `bluetape4k-dependencies` is the final consumer BOM and is released after all
  imported bluetape4k BOMs are visible. Do not use the final dependencies BOM as
  the source of internal release versions inside the same train.

Reference transition table:

| Phase | Internal reference example | Rule |
|---|---|---|
| Development | `bluetape4k = "1.9.2-SNAPSHOT"` | Consume the matching upstream snapshot line. |
| Release prep before upstream is public | keep `1.9.2-SNAPSHOT` | Stop; do not release downstream yet. |
| Release prep after upstream HTTP 200 | `bluetape4k = "1.9.2"` | Remove `-SNAPSHOT` and verify the exact artifact from Maven Central. |
| Post-release reopen | `bluetape4k = "1.9.3-SNAPSHOT"` or next active upstream snapshot | Return to snapshot consumption for development. |

### Gradle Catalog vs Consumer BOM

- `bluetape4k-dependencies/gradle/libs.versions.toml` is a build/contributor
  catalog source for external library and plugin alignment. Pin it by a git ref
  such as `catalog/YYYY-MM-DD-NN`.
- `io.github.bluetape4k:bluetape4k-dependencies` is the user-facing consumer
  BOM and uses semantic versions such as `1.1.3`.
- Use `bluetape4kDependenciesCatalogPath` or
  `bluetape4kDependenciesCatalogRef` for the build catalog source. Use
  `bluetape4kDependenciesVersion` only when importing the consumer BOM as a
  platform.

### Branch Lines

- `develop` is the active release line. Patch releases normally continue on
  `develop` until the patch milestone is closed or deferred.
- Create `release/X.Y.x` only when a previous minor line needs a hotfix after
  `develop` has advanced to the next minor line.
- Maintenance branches carry only bug, security, or compatibility fixes; every
  fix is forward-ported to `develop`.

## Branch Line Policy

Default to sequential development on `develop`. The `develop` branch represents
the currently active release line, including patch releases. Do not move
`develop` to the next minor version while an active patch milestone still owns
the next release, unless that patch milestone is explicitly closed or deferred.

Use maintenance branches only on demand:

- Create `release/X.Y.x` from the last released `X.Y.Z` tag only when a patch
  hotfix is needed after `develop` has already advanced to the next minor line.
- Set that maintenance branch to the next patch version, for example
  `baseVersion=1.9.3` from tag `1.9.2`.
- Apply only bug fixes, security fixes, and low-risk compatibility fixes to the
  maintenance branch.
- Release patch tags such as `1.9.3` from the maintenance branch.
- Forward-port every maintenance fix to `develop` by cherry-pick or merge.
- Do not backport next-minor feature/API work from `develop` into maintenance
  branches.

This keeps normal work simple while preserving the ability to patch a previous
minor line during the next minor development cycle.

Repository version line changes are governed by
`Version Management Policy > Repository Artifact Version`.

## Release Preconditions

Before running `Org Release Train` with `dryRun=false`:

- Shared version drift report has no unplanned drift.
- Each target repository has a matching release tag for the requested version.
- Target repositories have `snapshotVersion=` empty, and release workflows use
  `baseVersion` without injecting `-SNAPSHOT`.
- Internal `bluetape4k-*` references in release-prep branches use released
  upstream versions only; each referenced upstream artifact is publicly visible
  from Maven Central.
- Repository-local release workflows have passed in `dryRun` or diagnostic mode.
- Snapshot train has succeeded for the same dependency state.
- GitHub Packages publishing and signing secrets are valid in target repos.

## Snapshot Preconditions

Before running `Org Snapshot Dispatch` with `dryRun=false`:

- Target repositories are on the intended `develop` state.
- Target repositories have `snapshotVersion=` empty in `gradle.properties`; the
  snapshot workflow injects `-PsnapshotVersion=-SNAPSHOT`.
- Internal `bluetape4k-*` references on development branches use matching
  upstream `-SNAPSHOT` versions until release preparation removes the suffix.
- Snapshot artifact evidence uses Central snapshot repository metadata
  (`maven-metadata.xml` under `central.sonatype.com/repository/maven-snapshots`),
  not release Maven Central POM URLs.
- Version drift is either aligned or documented.
- Repositories that import the shared Gradle catalog read
  `bluetape4k-dependencies/gradle/libs.versions.toml` from a checked-out
  `bluetape4k-dependencies` ref through `bluetape4kDependenciesCatalogPath` or
  `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH`, or download the raw TOML pinned by
  `bluetape4kDependenciesCatalogRef` / `BLUETAPE4K_DEPENDENCIES_CATALOG_REF`.
- Nightly failures are understood or intentionally waived.
- The caller typed `deploy snapshots` in the confirmation input.

## Drift Policy

Organization-governed version groups are tracked by
`scripts/version_drift_report.py`:

- bluetape4k artifacts and bluetape4k-dependencies BOM
- `bluetape4k-dependencies/gradle/libs.versions.toml` as the
  build/contributor catalog source, pinned by a date-stamped
  `catalog/YYYY-MM-DD-NN` git ref when used across repos
- Kotlin
- Spring Boot
- Testcontainers
- Jackson 2 and Jackson 3
- Exposed
- Lettuce and Redisson
- AWS Kotlin SDK and Smithy Kotlin
- Kover
- Apache Fory

The same report also auto-discovers shared version aliases across
`bluetape4k-*` library repositories. If at least two library repositories
declare the same alias and the values differ, the report lists the drift and
marks the `bluetape4k-projects` value as the default baseline when present.

The report also fails compatibility-line alias violations. Aliases such as
`ignite`/`ignite3`, `kafka3`/`kafka4`, `spring-kafka`/`spring-kafka4`,
`jackson`/`jackson3`, and `spring-boot`/`spring-boot4` encode supported major
lines. A PR that changes `ignite` to 3.x or `spring-kafka4` to 3.x is invalid
even if the dependency coordinates resolve.

Allowed drift must be documented in the release notes or a linked issue before
release freeze. Experimental and Java 25-only modules may deviate when the
reason is explicit.

The drift report covers the main bluetape4k libraries plus governed
workshop/example repositories. `ocean-workshop` and `kotlin-dev-agent` are
intentionally excluded from this governance scope.

Governed workshop/example/application repositories should consume
`bluetape4k-dependencies` as their only bluetape4k version source. They should
not pin individual `io.github.bluetape4k*` artifact versions in
`gradle/libs.versions.toml`; artifact aliases should be versionless and resolved
through the BOM. See `docs/governance/dependency-governance.md` for the exact
consumer catalog shape and forbidden aliases.

For `bluetape4k-*` library repositories, keep build catalog consumption
separate from BOM consumption:

- Use `bluetape4kDependenciesCatalogPath` or
  `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH` for the checked-out
  `bluetape4k-dependencies/gradle/libs.versions.toml`; use
  `bluetape4kDependenciesCatalogRef` or
  `BLUETAPE4K_DEPENDENCIES_CATALOG_REF` when resolving the same TOML from a git
  ref.
- Use `bluetape4kDependenciesVersion` only when importing
  `io.github.bluetape4k:bluetape4k-dependencies` as a platform.
- Do not point a repository in the release train at a final BOM version that
  cannot exist until that same repository is released.
- During development, point internal `bluetape4k-*` references at the matching
  upstream `-SNAPSHOT` line. During release prep, remove `-SNAPSHOT` only after
  the upstream release has been published and verified from Maven Central.

## Dependency Update Validation

Dependabot is the update detector and PR generator. The central drift report is
the cross-repository consistency gate. Do not rely on Dependabot alone for
release readiness because it operates per repository.

Use this validation ladder:

| Change type | Required validation |
|---|---|
| Patch/minor library update scoped to one repository | Repository CI, then targeted Nightly only when the touched dependency is used by integration tests or runtime adapters. |
| Shared baseline update such as Kotlin, Spring Boot, Gradle, Testcontainers, Jackson, Redis clients, Exposed, AWS SDK, or Apache Fory | Repository CI plus affected repository Nightly. Dispatch all governed library Nightlies when the affected set is unclear. |
| Compatibility-line alias update such as `ignite`, `ignite3`, `kafka3`, `kafka4`, `spring-kafka`, or `spring-kafka4` | Verify the alias stays on its encoded major line. Reject cross-line updates and update the matching alias instead. |
| `bluetape4k-dependencies` BOM update | Version drift report plus Nightly for release/snapshot target repositories. |
| Major upgrade, compiler/plugin/runtime change, or release-freeze update | Version drift report, affected Nightly, and manual Weekly Full Nightly before release. |
| Documentation or GitHub Actions-only update | Workflow validation or repository CI only. |

If a dependency update can break another repository later, do not merge on CI
alone. Either run the affected Nightly before merge or document the deferred
Nightly run in the PR.

When `bluetape4k-projects` declares a shared runtime library alias, treat that
version as the default organization baseline. Major updates for Redis clients,
serialization libraries, persistence adapters, or other shared runtime
components should begin in `bluetape4k-projects` before individual repositories
advance.
