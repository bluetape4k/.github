# 2026-05-23 Release Train Audit

## Scope

Release candidate audit before publishing the post-`bluetape4k-projects 1.9.1`
train.

## Current Gate

Do not publish release artifacts until the milestone and version blockers below
are resolved.

## Milestone Gate

Each target release version must have a matching GitHub milestone before the
release PR/tag is prepared. The milestone check is version-specific; do not
infer readiness from a previous patch milestone, backlog milestone, or next
minor milestone.

For every target milestone, record:

- milestone existence;
- open issues assigned to that milestone;
- open PRs that close issues in that milestone;
- whether each open item is included in this release or explicitly deferred.

## Repository Status

| Repository | Target | Current local `baseVersion` | GitHub milestone state | Gate |
|---|---:|---:|---|---|
| `bluetape4k-projects` | `1.9.1` | `1.9.1` | exists, open: #620 | Hold until downstream handoff is complete |
| `bluetape4k-aws` | `0.2.1` | `0.2.1` | exists, open: 0 | Wait for `bluetape4k-exposed 1.9.1`, then bump exposed reference |
| `bluetape4k-text` | `0.1.2` | `0.1.2` | exists, open: 0 | Ready for validation |
| `bluetape4k-graph` | `0.4.1` | `0.4.1` | exists, open: 0 | Ready for validation; final dependencies BOM import removed |
| `bluetape4k-javers` | `0.1.2` | `0.1.2` | exists, open: 0 | Ready for validation |
| `bluetape4k-exposed` | `1.9.1` | `1.9.1` | exists, open: 0 | Ready for validation |
| `bluetape4k-leader` | `0.2.1` | `0.2.1` | exists, open: #270 | Resolve #270 PR; wait for `bluetape4k-exposed 1.9.1` if test helper reference is bumped |
| `bluetape4k-image` | `0.1.2` | `0.1.2` | exists, open: 0 | Wait for `bluetape4k-aws 0.2.1`, then bump aws reference |
| `bluetape4k-dependencies` | `1.1.3` | `1.1.2` | exists, open: 0 | Keep at `1.1.2` until final BOM step, then bump to `1.1.3` |

## Open Target Items

- `bluetape4k-projects 1.9.1`: #620 `chore: coordinate downstream BOM/catalog handoff after projects 1.9.1`.
- `bluetape4k-leader 0.2.1`: #270 `feat: promote StringTruncateSupport to bluetape4k-support after v1 stabilizes`.

## Non-Target Open Items To Defer Or Re-scope

- `bluetape4k-javers 0.2.0`: #3, #4, #5 are feature work and are not part of
  the proposed `0.1.2` patch release unless the release scope changes.
- `bluetape4k-exposed backlog`: #24, #30, #31, #32 are CockroachDB feature work
  and are not part of the proposed `1.9.1` patch release unless re-scoped.
- `bluetape4k-image Backlog`: #1, #2, #3, #4 are new feature work and are not
  part of the proposed `0.1.2` patch release unless re-scoped.
- `bluetape4k-graph backlog`: #30 is Neptune research/epic work and is not
  part of the proposed `0.4.1` patch release unless re-scoped.

## Internal Reference Preflight

Internal `bluetape4k-*` references must follow release order. If the referenced
repo is part of this release train, downstream repos must wait for that
upstream target version to be released and Maven Central HTTP 200. Do not use
the previous public release as a substitute. The shared catalog source ref is
only for external library/plugin version alignment.

Current Maven Central checks:

| Reference | Version | HTTP | Notes |
|---|---:|---:|---|
| `io.github.bluetape4k:bluetape4k-bom` | `1.9.1` | `200` | Published upstream for downstream repositories. |
| `io.github.bluetape4k.exposed:bluetape4k-exposed-bom` | `1.9.0` | `200` | Existing exposed release; if a downstream repo is in the same train and needs exposed `1.9.1`, it must wait for exposed `1.9.1` HTTP 200. |
| `io.github.bluetape4k.aws:bluetape4k-aws-bom` | `0.2.0` | `200` | Existing aws release; image must wait for aws `0.2.1` HTTP 200 if image consumes the new train version. |
| `io.github.bluetape4k:bluetape4k-dependencies` | `1.1.1` | `200` | Existing final BOM; do not use it to shortcut this train. |

Current release worktree reference state:

| Repository | Internal references observed | Gate |
|---|---|---|
| `bluetape4k-aws` | `bluetape4k-bom 1.9.1`, `bluetape4k-exposed-bom 1.9.0` | WAIT: `aws-exposed` uses exposed, so release `exposed 1.9.1` first and then bump aws. |
| `bluetape4k-text` | `bluetape4k-bom 1.9.1` | PASS. |
| `bluetape4k-graph` | `bluetape4k-bom 1.9.1` | PASS; final `bluetape4k-dependencies` BOM import removed. |
| `bluetape4k-javers` | `bluetape4k-bom 1.9.1`; no current exposed build/catalog reference | PASS for this train. Future `javers-exposed` work must move javers behind exposed. |
| `bluetape4k-exposed` | `bluetape4k-bom 1.9.1` | PASS. |
| `bluetape4k-leader` | `bluetape4k-bom 1.9.1`, `bluetape4k-exposed 1.9.0` test helpers | WAIT if exposed test helpers must follow train; otherwise #270 validation can proceed. |
| `bluetape4k-image` | `bluetape4k-bom 1.9.1`, `bluetape4k-aws-bom 0.2.0` | WAIT: release aws `0.2.1`, verify HTTP 200, then bump image. |

## Required Order

1. Resolve release-scope issues in each target milestone.
2. For missing target milestones, create the milestone before opening or moving
   release-prep issues. Done for this train.
3. Bump each repository `baseVersion` to the target version before release PR.
   Done for library repos; defer `bluetape4k-dependencies 1.1.3` until the
   final BOM step.
4. Keep `bluetape4k-dependencies` catalog source refs such as
   `catalog/2026-05-23-00` only for shared external library/plugin version
   alignment, and consume them through a checked-out
   `gradle/libs.versions.toml`.
5. For internal `bluetape4k-*` dependencies, reference the newly published
   upstream release version explicitly; do not use the catalog source ref as
   that version source.
6. Release libraries in dependency order:
   `projects 1.9.1` -> `exposed 1.9.1`, `text 0.1.2`, `graph 0.4.1`,
   `javers 0.1.2` -> `aws 0.2.1`, `leader 0.2.1` -> `image 0.1.2` ->
   `dependencies 1.1.3`.
7. Release `bluetape4k-dependencies 1.1.3` last, after all imported BOMs return
   HTTP 200 from Maven Central.

The order above is valid only for the audited 2026-05-23 worktrees. Re-scan
dependencies for every future train. In particular, planned `javers-exposed`
work will make `bluetape4k-javers` depend on `bluetape4k-exposed`; at that
point `javers` must wait for the target exposed release and Maven Central HTTP
200.

## Immediate Blocker

`bluetape4k-leader` issue #270 must be completed before `0.2.1` is released:
replace the local `leader-core` UTF-8 truncation helper with
`io.bluetape4k.support.truncateUtf8` from `bluetape4k-projects 1.9.1`.

## Catalog Source Correction

The internal Gradle catalog should not be published as a Maven Central
artifact. It is a build input for `bluetape4k-*` repositories, so the release
train should pin `bluetape4k-dependencies/gradle/libs.versions.toml` by a
`bluetape4k-dependencies` git ref and pass that checked-out file path to
downstream builds.

Validated on 2026-05-23:

- `bluetape4k-dependencies` NMCP zip generation contains only
  `io/github/bluetape4k/bluetape4k-dependencies/1.1.2/*`; no version-catalog
  publication is generated.
- `projects`, `aws`, `text`, `graph`, `javers`, `exposed`, `leader`, and
  `image` all passed `./gradlew help` with
  `-Pbluetape4kDependenciesCatalogPath=<dependencies-worktree>/gradle/libs.versions.toml`.
- `aws`, `text`, and `leader` also passed `./gradlew help` with no path
  override after deleting the local downloaded TOML cache; Gradle resolved the
  catalog from the `bluetape4k-dependencies` git ref fallback.
