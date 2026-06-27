# bluetape4k WIP

Snapshot: 2026-06-27 KST
Scope: internal bluetape4k library release train that culminates in
`bluetape4k-dependencies 1.3.0`.

## Release Target Rule

For every publishable repository, the release target is always the next semantic
version milestone after the latest GitHub release.

Do not infer a stable release target from the current snapshot catalog or from a
repository's already-bumped `baseVersion`. Those values can be ahead of the
release boundary and must be aligned back to the target milestone before
publishing.

## Release Train Checklist Rule

This section supersedes the older one-repo-at-a-time stable release plan below.
Use it for the next bluetape4k release train.

### Why

The 2026-06-27 `bluetape4k-dependencies 1.3.0` run exposed a release-process
failure: stable publication started before the final issue/artifact checklist
was explicit. The release workflow published the BOM before the GitHub Release
job was cancelled. The durable fix is a checklist-gated train, not operator
memory.

### Required Train Shape

1. Build the complete target inventory first:
   - repo, version, branch/SHA, release class, milestone, release workflow, and
     expected artifacts;
   - expected artifacts must distinguish Maven Central publications from
     git-ref build contracts. `bluetape4k-dependencies` publishes the BOM to
     Maven Central, while the Gradle version catalog is consumed from a
     checked-out git ref or catalog tag by ecosystem repositories;
   - generated POM license must be MIT for bluetape4k ecosystem artifacts unless
     a written repo-local exception exists.
2. Close the issue/PR gate before any stable tag:
   - target milestone open issues are 0;
   - open PRs for the target branch/version are 0;
   - open issues without the milestone that mention the target version, release,
     catalog, BOM, publication, or planned artifact are either closed or
     explicitly moved out of scope with a comment.
3. Run the complete snapshot train first:
   - validate `projects -> exposed/aws/text/graph/leader/javers/image ->
     dependencies` with snapshot/candidate catalog state before any stable
     publication;
   - if a downstream repo exposes a shared-version, catalog, artifact, license,
     or workflow problem, fix it and rerun the affected snapshot validation;
   - only proceed when the whole selected topology is green.
4. Run stable releases after the snapshot train is green:
   - stable releases may be parallelized for repos whose release DAG edges are
     already validated and whose stable workflows do not mutate shared catalog
     state;
   - keep sequential Maven Central HTTP 200 gates only where a downstream stable
     release consumes an upstream stable artifact directly.
5. Hold before irreversible dispatch:
   - immediately before tag push or workflow dispatch, report the checklist rows
     for open issues, open PRs, tag absence, release absence, workflow input
     schema, expected artifact matrix, POM MIT license, missing dependency
     versions, and `-SNAPSHOT` absence;
   - if any row is failed, stale, or unknown, stop and repair before dispatch.
6. Handle partial publication explicitly:
   - if Maven Central publication succeeds before cancellation, treat that
     version as consumed; do not retag or republish the same version;
   - if the artifact matrix is correct and only GitHub Release creation was
     cancelled, create the GitHub Release manually after Maven Central HTTP 200;
   - if the artifact matrix is incomplete, publish the smallest patch release
     that fixes the missing artifact/metadata.
7. Sync Maven BOM consumers after the final dependencies BOM is visible:
   - do not update workshops/examples/apps before the target
     `bluetape4k-dependencies` BOM is Maven Central HTTP 200;
   - after visibility, update `bluetape4k-workshop`, `exposed-workshop`,
     `exposed-r2dbc-workshop`, `clinic-appointment`, and `timefold-workshop`
     to the final dependencies version, or record a repo-specific out-of-scope
     reason;
   - verify each consumer with the lightest dependency-resolution/build check
     that proves the BOM upgrade works.

### `dependencies 1.3.0` Incident State

- Tag `1.3.0` was pushed at
  `67106343402079bf01d7b6304f21aab5afa14d6c`.
- Release workflow `28299496636` published the Maven Central BOM job before
  cancellation; GitHub Release creation was cancelled.
- Issue `bluetape4k-dependencies#126` is closed. The
  `bluetape4k-exposed-ktor` alias is present in tag `1.3.0`, but the issue was
  not closed before stable dispatch, which is the process failure this checklist
  prevents.
- The current `build.gradle.kts` POM license metadata still says Apache License
  2.0 and must be changed to MIT in the next patch release.
- The Gradle version catalog is an ecosystem build-contract source consumed
  from a checked-out git ref or catalog tag. It is not a Maven Central
  publication; verify the ref/source state in the next patch release.
- Workshop/example/app consumers were promoted from
  `bluetape4k-dependencies 1.2.0` to `1.3.1` after the patch BOM became Maven
  Central-visible. Do not substitute a later patch version for example repos
  unless the user explicitly changes the consumer-sync target.
- Consumer sync PRs merged on 2026-06-28 KST:
  `bluetape4k-workshop` #315, `exposed-workshop` #136,
  `exposed-r2dbc-workshop` #111, `clinic-appointment` #155, and
  `timefold-workshop` #42. Each repo was locally verified with
  `./gradlew test --no-daemon --no-configuration-cache --no-build-cache`
  before PR creation, and GitHub checks passed before merge.

## Current Target Matrix

Verified with live GitHub releases, GitHub milestones, local
`gradle.properties`, `bluetape4k-dependencies/gradle/libs.versions.toml`, and
Maven Central HTTP checks on 2026-06-27 KST.

| Repo | Latest release | Next milestone | Milestone state | Open issues | Open PRs | Current `baseVersion` | Catalog / BOM line | Maven Central | Readiness |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| `bluetape4k-projects` | `1.11.0` | released | closed | 0 | 0 | `1.11.0` | `1.11.0` | 200 | Released on 2026-06-27; downstream gates may consume projects `1.11.0` |
| `bluetape4k-exposed` | `1.11.0` | released | closed | 0 | 0 | `1.11.0` | `1.11.0` | 200 | Released on 2026-06-27; downstream gates may consume exposed `1.11.0` |
| `bluetape4k-aws` | `0.4.0` | released | closed | 0 | 0 | `0.4.0` | `0.4.0` | 200 | Released on 2026-06-27; downstream image gate may consume AWS `0.4.0` |
| `bluetape4k-image` | `0.2.0` | `0.3.0` | open | 0 | 0 | `0.3.0` | `0.3.0-SNAPSHOT` | 404 | Release prep: AWS stable artifact is visible; changelog and release gates remain |
| `bluetape4k-text` | `0.2.1` | released | closed | 0 | 0 | `0.2.1` | `0.2.1` | 200 | Released on 2026-06-27; downstream gates may consume text `0.2.1` |
| `bluetape4k-graph` | `0.5.1` | released | closed | 0 | 0 | `0.6.0` on `develop`, `0.5.1` on release-only branch | `0.5.1` | 200 | Released on 2026-06-27 from release-only branch; downstream gates may consume graph `0.5.1` |
| `bluetape4k-leader` | `0.4.0` | released | closed | 0 | 0 | `0.4.0` | `0.4.0` | 200 | Released on 2026-06-27; downstream gates may consume leader `0.4.0` |
| `bluetape4k-javers` | `0.2.1` | released | closed | 0 | 0 | `0.3.0` on `develop`, `0.2.1` on release-only branch | `0.2.1` | 200 | Released on 2026-06-27 from release-only branch; downstream gates may consume javers `0.2.1` |
| `bluetape4k-dependencies` | `1.2.0` | `1.3.0` | open | 0 | 0 | `1.3.0` | self | 404 | Final train artifact; blocked by internal BOM releases |

## Immediate Corrections From This Recheck

- `bluetape4k-text` target is `0.2.1`, not `0.3.0`.
- `bluetape4k-graph` target is `0.5.1`, not `0.6.0`.
- `bluetape4k-javers` target is `0.2.1`, not `0.3.0`.
- `bluetape4k-text 0.2.1` is released. Milestone `0.2.1` is closed with 0
  open issues, GitHub Release `0.2.1` exists, and Maven Central returns HTTP
  200 for `io.github.bluetape4k.text:bluetape4k-text-bom:0.2.1`.
- `bluetape4k-projects 1.11.0` is released. Milestone `1.11.0` is closed with
  0 open issues, GitHub Release `1.11.0` exists, and Maven Central returns HTTP
  200 for `io.github.bluetape4k:bluetape4k-bom:1.11.0`.
- `bluetape4k-exposed 1.11.0` is released. Milestone `1.11.0` is closed with
  0 open issues, GitHub Release `1.11.0` exists, and Maven Central returns HTTP
  200 for `io.github.bluetape4k.exposed:bluetape4k-exposed-bom:1.11.0`.

## Current CI Evidence

Latest relevant `develop` workflow evidence:

| Repo | Evidence |
|---|---|
| `bluetape4k-projects` | PR #932 merged; PR #933 fixed Kafka 4 test ABI. Nightly/full PASS `28291373721`, Publish Snapshot PASS `28291694898`, Release PASS `28291920425`, Maven Central HTTP 200 for `bluetape4k-bom:1.11.0` |
| `bluetape4k-exposed` | PR #328 and #329 merged. Nightly/full PASS `28292715331`, Publish Snapshot PASS `28292977136`, Release PASS `28293137346`, Maven Central HTTP 200 for `bluetape4k-exposed-bom:1.11.0` |
| `bluetape4k-aws` | PR #315 merged. Nightly/full PASS `28296169769`, Publish Snapshot PASS `28296360347`, Release PASS `28296483773`, Maven Central HTTP 200 for `bluetape4k-aws-bom:0.4.0` and `bluetape4k-aws-java:0.4.0` |
| `bluetape4k-image` | Examples and Publish Snapshot PASS on `develop` on 2026-06-26; Code Quality failure exists on `develop` on 2026-06-27 |
| `bluetape4k-text` | PR #152 merged. Nightly/full PASS `28293689170`, Publish Snapshot PASS `28293791294`, Release PASS `28293879266`, Maven Central HTTP 200 for `bluetape4k-text-bom:0.2.1` |
| `bluetape4k-graph` | Release-only branch `release/graph-0.5.1-prep` released. Nightly/full PASS `28294573268`, Publish Snapshot PASS `28294814367`, Release PASS `28294931874`, Maven Central HTTP 200 for `bluetape4k-graph-bom:0.5.1` and `bluetape4k-graph-core:0.5.1` |
| `bluetape4k-leader` | PR #543 merged. Nightly/full PASS `28297066895`, Publish Snapshot PASS `28297329537`, Release PASS `28297441418`, Maven Central HTTP 200 for `bluetape4k-leader-bom:0.4.0` and `bluetape4k-leader-core:0.4.0` |
| `bluetape4k-javers` | Release-only branch `release/javers-0.2.1-prep` released. Nightly/full PASS `28295424149`, Publish Snapshot PASS `28295579016`, Release PASS `28295671657`, Maven Central HTTP 200 for `bluetape4k-javers-bom:0.2.1` and `javers-core:0.2.1` |
| `bluetape4k-dependencies` | CI and Automatic Dependency Submission PASS on `develop` on 2026-06-26; final release CI must be rerun on the release-prep SHA |

Re-run or replace stale Nightly/Snapshot evidence before stable release dispatch.

## 2026-06-27 Release-Prep Documentation Pass

The issue work is complete, but release documentation and metadata were not
finished. The active pre-release work is therefore docs/config hygiene, not
stable publication.

Prepared worktrees:

| Repo | Branch | Scope |
|---|---|---|
| `bluetape4k-projects` | `release/projects-1.11.0-prep` | Add `CHANGELOG.md` `1.11.0` section. |
| `bluetape4k-exposed` | `release/exposed-1.11.0-prep` | Add `CHANGELOG.md` `1.11.0`; update README dependency snippets to `1.11.0`. |
| `bluetape4k-aws` | `release/aws-0.4.0-prep` | Refresh `CHANGELOG.md` `0.4.0` release date/evidence. |
| `bluetape4k-image` | `release/image-0.3.0-prep` | Add `CHANGELOG.md` `0.3.0`; replace README placeholders with `0.3.0`. |
| `bluetape4k-text` | `release/text-0.2.1-prep` | Align README quality-gate wording with `0.2.1`. |
| `bluetape4k-graph` | `release/graph-0.5.1-prep` | Release-only branch from tag `0.5.0`; set `baseVersion=0.5.1`; update changelog and README snippets. |
| `bluetape4k-leader` | `release/leader-0.4.0-prep` | Add `CHANGELOG.md` `0.4.0`; update README snippets to `0.4.0`. |
| `bluetape4k-javers` | `release/javers-0.2.1-prep` | Release-only branch from tag `0.2.0`; set `baseVersion=0.2.1`; update changelog and README snippets. |
| `bluetape4k-dependencies` | `release/dependencies-1.3.0-prep` | Add `CHANGELOG.md` `1.3.0`; update README target matrix only. Do not pin `gradle/libs.versions.toml` to stable until upstream artifacts are Maven Central-visible. |

Validation so far:

- `git diff --check` passed in all 9 release-prep worktrees.
- Targeted scans found no accidental `Unreleased after ...` headings or README
  `<version>` placeholders in release snippets; remaining `SNAPSHOT` and older
  version references are historical changelog entries, snapshot usage docs, or
  intentionally retained development catalog values.

PR policy:

- `bluetape4k-projects` release-prep PR #932 and release-blocker PR #933 are
  merged. `bluetape4k-projects 1.11.0` is released and Maven Central-visible.
- `bluetape4k-exposed` release-prep PR #328 and release-blocker PR #329 are
  merged. `bluetape4k-exposed 1.11.0` is released and Maven Central-visible.
- `bluetape4k-text` release-prep PR #152 is merged. `bluetape4k-text 0.2.1`
  is released and Maven Central-visible.
- `bluetape4k-dependencies` release-prep branch now contains stable
  `bluetape4k-bom=1.11.0`, `bluetape4k-exposed-bom=1.11.0`, and
  `bluetape4k-text-bom=0.2.1`, `bluetape4k-graph-bom=0.5.1`,
  `bluetape4k-javers-bom=0.2.1`, and `bluetape4k-aws-bom=0.4.0`.
  Published catalog refs:
  `catalog/2026-06-27-00` after projects `1.11.0`, and
  `catalog/2026-06-27-01` after exposed `1.11.0`, and
  `catalog/2026-06-27-02` after text `0.2.1`, and
  `catalog/2026-06-27-03` after graph `0.5.1`, and
  `catalog/2026-06-27-04` after javers `0.2.1`, and
  `catalog/2026-06-27-05` after AWS `0.4.0`, and
  `catalog/2026-06-27-06` after leader `0.4.0`.
- Develop-based downstream docs-prep branches were pushed for review context but
  must stay draft until the publish train reaches that repository:
  `bluetape4k-image` #221 and `bluetape4k-dependencies` #131.
- `graph 0.5.1` and `javers 0.2.1` are release-only branches from prior tags.
  Do not open them as ordinary `develop` PRs because that would mix patch
  release state with the next development line.
- `bluetape4k-aws` release-prep PR #315 is merged. `bluetape4k-aws 0.4.0` is
  released and Maven Central-visible.
- `bluetape4k-leader` release-prep PR #543 is merged. `bluetape4k-leader
  0.4.0` is released and Maven Central-visible.
- Do not merge, mark ready, or publish any remaining downstream PR before the
  upstream Maven Central HTTP 200 gate required by `$bluetape4k-publish` has
  passed.

## Projects-Ready Internal Release Train Plan

Use this plan only after `bluetape4k-projects 1.11.0` is genuinely ready:
milestone open issues are 0, open PRs are 0, reviews and review threads are
clear, `CHANGELOG.md` has a `1.11.0` section, CI is green on the target SHA,
Nightly/full has passed on the target SHA or a dated waiver is recorded, and a
snapshot publish/consume validation exists for the same dependency state.

### Stable Release Flow

Primary flow: sequential internal `repo-release` gates, followed by the final
`dependencies-minor-train` release for `bluetape4k-dependencies 1.3.0`.

Execution model:

1. Release exactly one internal repository at a time.
2. After each stable repo release, wait for Maven Central HTTP 200 for the BOM
   POM and at least one representative module POM.
3. Update `bluetape4k-dependencies` `develop` to consume the newly published
   stable BOM before moving to the next downstream validation step.
4. Treat `bluetape4k-dependencies 1.3.0` as the final BOM/catalog artifact, not
   as the whole release train. Do not publish it until every selected internal
   BOM is non-SNAPSHOT and Maven Central-visible.
5. Do not use release workflow test skips unless the exact release SHA already
   has fresh Nightly/full and snapshot validation evidence recorded in this
   file or in the repo-local WIP.

### Per-Repository Gate

Before dispatching a stable release workflow for any internal repo:

- Re-read the target repo's `.github/workflows/release.yml` and pass only
  declared `workflow_dispatch` inputs.
- Verify `snapshotVersion=` is empty.
- Verify `baseVersion` equals the target stable version. For repos already
  bumped ahead of the target, create a release-prep branch that restores the
  exact target source state before dispatch.
- Verify target milestone open issues are 0 and open PRs are 0.
- Re-read PR reviews and review threads for the final release-prep PR.
- Verify `CHANGELOG.md` has the target dated section.
- Verify no generated POM, catalog ref, or release artifact metadata contains
  unintended `-SNAPSHOT`.
- Run or verify CI, Nightly/full, and snapshot publish/consume validation on
  the exact target SHA.

Stop immediately if any gate fails, if a target version differs from the root
matrix, if Maven Central returns non-200 for a required upstream BOM, or if a
new review/comment appears after the last check.

### Internal Release Order After Projects

1. `bluetape4k-projects 1.11.0`: release first; it is the upstream foundation
   for several downstream repos.
2. `bluetape4k-exposed 1.11.0`: release after projects `1.11.0` is Maven
   Central-visible.
3. `bluetape4k-text 0.2.1`: released and Maven Central-visible; development
   remains on the `0.3.0` line after the patch release.
4. `bluetape4k-graph 0.5.1`: restore target source alignment from the current
   `0.6.0` development line, release `0.5.1`, then keep development on the
   existing `0.6.0` line.
5. `bluetape4k-javers 0.2.1`: restore target source alignment from the current
   `0.3.0` development line, release `0.2.1`, then keep development on the
   existing `0.3.0` line.
6. `bluetape4k-aws 0.4.0`: released and Maven Central-visible.
7. `bluetape4k-leader 0.4.0`: released and Maven Central-visible.
8. `bluetape4k-image 0.3.0`: release after AWS stable artifacts are visible.
9. `bluetape4k-dependencies 1.3.0`: publish only after all selected internal
   BOM refs are pinned to stable, Maven Central-visible versions.

### Final Dependencies Gate

Before `bluetape4k-dependencies 1.3.0` dispatch:

- `gradle/libs.versions.toml` internal BOM refs must be exactly:
  `bluetape4k-bom=1.11.0`, `bluetape4k-exposed-bom=1.11.0`,
  `bluetape4k-aws-bom=0.4.0`, `bluetape4k-image-bom=0.3.0`,
  `bluetape4k-text-bom=0.2.1`, `bluetape4k-graph-bom=0.5.1`,
  `bluetape4k-leader-bom=0.4.0`, and `bluetape4k-javers-bom=0.2.1`.
- `CHANGELOG.md` must have a `1.3.0` section.
- `scripts/sync-shared-versions.py --workspace .. --check --summary` must pass.
- Managed catalog/artifact verification must pass without `--allow-snapshots`.
- Final CI, dependency-submission, and snapshot validation must pass on the
  exact release catalog state.

### Plan Validation Evidence

This plan was refreshed on 2026-06-26 KST with:

- GNO GitHub history query for prior dependencies release-train PRs, including
  dependencies PR #67, #94, #100, and projects PR #689.
- GNO docs query for dependencies version-management guidance and the
  `1.3.0` snapshot-train lesson.
- Live GitHub release checks for every publishable repo; latest stable releases
  match the current target matrix.
- Live GitHub milestone checks for every target version; projects `1.11.0`,
  text `0.2.1`, graph `0.5.1`, and javers `0.2.1` currently have 0 open
  issues.
- Maven Central HTTP checks for `1.3.0` candidate BOMs; released BOMs return
  200 and unreleased BOMs still return 404, which is expected before their
  stable dispatch.
- Local `repo-status` checks for all publishable repos; every checked repo is
  clean on `develop` and aligned with `origin/develop`.

## Active Release Work

### 1. bluetape4k-projects `1.11.0`

Status:

- Released on 2026-06-27.
- PR #932 merged the release-prep `CHANGELOG.md` `1.11.0` section.
- First Nightly/full run `28290549379` failed in `Test / Infra
  (kafka-resilience)` because Kafka `4.3.1` removed the
  `KafkaClusterTestKit.clientProperties()` ABI required by
  `spring-kafka-test 4.1.0`.
- PR #933 aligned `kafka4` to `4.2.1`; PR CI passed and the PR was merged as
  `6187173b58e8b4c5c435c145e00e94708f31ef75`.
- Nightly/full rerun `28291373721` passed on `6187173b`.
- Publish Snapshot run `28291694898` passed on `6187173b`.
- Release tag `1.11.0` was pushed at `6187173b`; release workflow
  `28291920425` passed and created GitHub Release `1.11.0`.
- Maven Central returned HTTP 200 for
  `https://repo1.maven.org/maven2/io/github/bluetape4k/bluetape4k-bom/1.11.0/bluetape4k-bom-1.11.0.pom`.
- Milestone `1.11.0` is closed with 0 open issues.

### 2. bluetape4k-text `0.2.1`

Status:

- Released on 2026-06-27.
- PR #152 merged the release-prep README and catalog-alignment changes.
- Nightly/full run `28293689170` passed on `2db7671`.
- Publish Snapshot run `28293791294` passed on `2db7671`.
- Release tag `0.2.1` was pushed at `2db7671`; release workflow
  `28293879266` passed and created GitHub Release `0.2.1`.
- Maven Central returned HTTP 200 for
  `https://repo1.maven.org/maven2/io/github/bluetape4k/text/bluetape4k-text-bom/0.2.1/bluetape4k-text-bom-0.2.1.pom`.
- Milestone `0.2.1` is closed with 0 open issues.
- Dependencies catalog ref `catalog/2026-06-27-02` pins
  `bluetape4k-text-bom=0.2.1`.

### 3. bluetape4k-graph `0.5.1`

Status:

- Released on 2026-06-27 from release-only branch
  `release/graph-0.5.1-prep`.
- Release branch pins `baseVersion=0.5.1`, `snapshotVersion=`,
  `bluetape4k=1.11.0`, and `catalog/2026-06-27-02`.
- Nightly/full run `28294573268` passed on `3e0fa7c`.
- Publish Snapshot run `28294814367` passed on `3e0fa7c`.
- Release tag `0.5.1` was pushed at `3e0fa7c`; release workflow
  `28294931874` passed and created GitHub Release `0.5.1`.
- Maven Central returned HTTP 200 for
  `https://repo1.maven.org/maven2/io/github/bluetape4k/graph/bluetape4k-graph-bom/0.5.1/bluetape4k-graph-bom-0.5.1.pom`
  and for representative module `bluetape4k-graph-core:0.5.1`.
- Milestone `0.5.1` is closed with 0 open issues.
- Dependencies catalog ref `catalog/2026-06-27-03` pins
  `bluetape4k-graph-bom=0.5.1`.
- `develop` remains on the `0.6.0` development line.

### 4. bluetape4k-javers `0.2.1`

Status:

- Released on 2026-06-27 from release-only branch
  `release/javers-0.2.1-prep`.
- Release branch pins `baseVersion=0.2.1`, `snapshotVersion=`,
  `bluetape4k=1.11.0`, and `catalog/2026-06-27-03`.
- Nightly/full run `28295424149` passed on `bffe194`.
- Publish Snapshot run `28295579016` passed on `bffe194`.
- Release tag `0.2.1` was pushed at `bffe194`; release workflow
  `28295671657` passed and created GitHub Release `0.2.1`.
- Maven Central returned HTTP 200 for
  `https://repo1.maven.org/maven2/io/github/bluetape4k/javers/bluetape4k-javers-bom/0.2.1/bluetape4k-javers-bom-0.2.1.pom`
  and for representative module `javers-core:0.2.1`.
- Milestone `0.2.1` is closed with 0 open issues.
- Dependencies catalog ref `catalog/2026-06-27-04` pins
  `bluetape4k-javers-bom=0.2.1` and omits the later
  `javers-spring-boot4-autoconfigure` alias because that artifact is not
  published in `0.2.1`.
- `develop` remains on the `0.3.0` development line.

### 5. bluetape4k-aws `0.4.0`

Status:

- Released on 2026-06-27.
- PR #315 merged the release-prep documentation and catalog-alignment changes.
- Release branch pins `baseVersion=0.4.0`, `snapshotVersion=`,
  `bluetape4k=1.11.0`, `bluetape4k-exposed=1.11.0`, and
  `catalog/2026-06-27-04`.
- Nightly/full run `28296169769` passed on `be4e6dae`.
- Publish Snapshot run `28296360347` passed on `be4e6dae`.
- Release tag `0.4.0` was pushed at `be4e6dae`; release workflow
  `28296483773` passed and created GitHub Release `0.4.0`.
- Maven Central returned HTTP 200 for
  `https://repo1.maven.org/maven2/io/github/bluetape4k/aws/bluetape4k-aws-bom/0.4.0/bluetape4k-aws-bom-0.4.0.pom`
  and for representative module `bluetape4k-aws-java:0.4.0`.
- Milestone `0.4.0` is closed with 0 open issues.
- Dependencies catalog ref `catalog/2026-06-27-05` pins
  `bluetape4k-aws-bom=0.4.0`.

### 6. bluetape4k-leader `0.4.0`

Status:

- Released on 2026-06-27.
- PR #543 merged the release-prep documentation and catalog-alignment changes.
- Release branch pins `baseVersion=0.4.0`, `snapshotVersion=`,
  `bluetape4k=1.11.0`, `bluetape4k-exposed=1.11.0`, and
  `catalog/2026-06-27-05`.
- Nightly/full run `28297066895` passed on `17ab7f87`.
- Publish Snapshot run `28297329537` passed on `17ab7f87`.
- Release tag `0.4.0` was pushed at `17ab7f87`; release workflow
  `28297441418` passed and created GitHub Release `0.4.0`.
- Maven Central returned HTTP 200 for
  `https://repo1.maven.org/maven2/io/github/bluetape4k/leader/bluetape4k-leader-bom/0.4.0/bluetape4k-leader-bom-0.4.0.pom`
  and for representative module `bluetape4k-leader-core:0.4.0`.
- Milestone `0.4.0` is closed with 0 open issues.
- Dependencies catalog ref `catalog/2026-06-27-06` pins
  `bluetape4k-leader-bom=0.4.0`.

## Release-Prep Repositories

These repositories have the correct next milestone by the latest-release rule
and no open target milestone issues, but still need normal release-prep gates.

### bluetape4k-exposed `1.11.0`

- Released on 2026-06-27.
- Milestone `1.11.0`: closed, 0 open issues.
- Current `baseVersion=1.11.0`.
- Catalog points `bluetape4k-exposed-bom` to `1.11.0` on
  `catalog/2026-06-27-01`.
- Release-prep branch has `CHANGELOG.md` `1.11.0` and README snippets aligned
  to `1.11.0`.
- Release workflow `28293137346` passed and Maven Central returned HTTP 200 for
  `bluetape4k-exposed-bom:1.11.0`.

### bluetape4k-aws `0.4.0`

- Released on 2026-06-27.
- Milestone `0.4.0`: closed, 0 open issues.
- Current `baseVersion=0.4.0`.
- Catalog points `bluetape4k-aws-bom` to `0.4.0` on
  `catalog/2026-06-27-05`.
- `CHANGELOG.md` has a `0.4.0` section.
- Release workflow `28296483773` passed and Maven Central returned HTTP 200 for
  `bluetape4k-aws-bom:0.4.0` and `bluetape4k-aws-java:0.4.0`.

### bluetape4k-image `0.3.0`

- Milestone `0.3.0`: open, 0 open issues.
- Current `baseVersion=0.3.0`.
- Catalog points `bluetape4k-image-bom` to `0.3.0-SNAPSHOT`.
- Release-prep branch has `CHANGELOG.md` `0.3.0` and README snippets aligned
  to `0.3.0`.
- Release after required AWS artifact is Maven Central visible.

### bluetape4k-leader `0.4.0`

- Released on 2026-06-27.
- Milestone `0.4.0`: closed, 0 open issues.
- Current `baseVersion=0.4.0`.
- Catalog points `bluetape4k-leader-bom` to `0.4.0` on
  `catalog/2026-06-27-06`.
- Release-prep branch has `CHANGELOG.md` `0.4.0` and README snippets aligned
  to `0.4.0`.
- Release workflow `28297441418` passed and Maven Central returned HTTP 200 for
  `bluetape4k-leader-bom:0.4.0` and `bluetape4k-leader-core:0.4.0`.

## bluetape4k-dependencies `1.3.0`

`bluetape4k-dependencies` is the final train artifact.

Blockers:

- Final release CI must be rerun on the exact release-prep SHA.
- Release-prep branch has `CHANGELOG.md` `1.3.0` and README target matrix
  aligned to the intended internal BOM versions.
- Unreleased internal BOM refs still point at snapshots.
- `bluetape4k-image-bom` still points at a snapshot until its own release gate
  passes.
- `scripts/sync-shared-versions.py --workspace .. --check --summary` now passes
  on the release-prep branch after projects, exposed, text, graph, javers, and
  AWS, and leader catalog promotions.

Before release:

1. Publish or intentionally align every internal BOM to the next milestone after
   its latest release.
2. Replace all internal `*-SNAPSHOT` BOM refs with Maven Central-visible stable
   versions.
3. Resolve shared-version drift.
4. Keep the `CHANGELOG.md` `1.3.0` section and README target matrix current.
5. Verify generated artifacts have no `-SNAPSHOT` and no missing dependency
   versions.
6. Run final CI, Nightly/full equivalent, and snapshot validation for the exact
   final catalog state.

## Next Patch Train: bluetape4k-dependencies `1.3.1`

Plan `1.3.1` as a selective patch train after `1.3.0` is released and Maven
Central visible.

Scope:

- Promote only `bluetape4k-javers` from `0.2.1` to `0.3.0`.
- Promote only `bluetape4k-text` from `0.2.1` to `0.3.0`.
- Promote only `bluetape4k-graph` from `0.5.1` to `0.6.0`.
- Retain all other bluetape4k BOM versions exactly as published in
  `dependencies 1.3.0`, unless the user explicitly changes the scope.

Preconditions:

- `bluetape4k-dependencies 1.3.0` is released and Maven Central returns HTTP
  200.
- `bluetape4k-javers 0.3.0`, `bluetape4k-text 0.3.0`, and
  `bluetape4k-graph 0.6.0` have closed target milestones, clean release
  preflight, and Maven Central-visible stable BOM artifacts.
- No unrelated internal BOM or external dependency version is changed in the
  `1.3.1` release prep PR.

Validation focus:

- Diff `gradle/libs.versions.toml` and generated managed catalog artifacts to
  confirm only the three planned BOM lines changed.
- Run `scripts/sync-shared-versions.py --workspace .. --check --summary` after
  the three downstream repos are aligned.
- Run `scripts/verify-managed-artifacts.py --summary` without
  `--allow-snapshots`.
- Verify final `1.3.1` CI and snapshot validation on the exact release catalog
  state before stable release dispatch.

## Recommended Execution Order

1. Done: `bluetape4k-projects 1.11.0` release-prep gates, Nightly/full, and
   snapshot validation passed on the final SHA.
2. Done: `bluetape4k-projects 1.11.0` is released and Maven Central returns
   HTTP 200 for the BOM POM.
3. Done: `bluetape4k-exposed 1.11.0` is released and Maven Central returns
   HTTP 200 for the BOM POM.
4. Done: `bluetape4k-text 0.2.1` is released and Maven Central returns HTTP
   200 for the BOM POM.
5. Done: `bluetape4k-graph 0.5.1` is released and Maven Central returns HTTP
   200 for the BOM and representative module POM.
6. Done: `bluetape4k-javers 0.2.1` is released and Maven Central returns HTTP
   200 for the BOM and representative module POM.
7. Done: `bluetape4k-aws 0.4.0` is released and Maven Central returns HTTP
   200 for the BOM and representative module POM.
8. Done: `bluetape4k-leader 0.4.0` is released and Maven Central returns HTTP
   200 for the BOM and representative module POM.
9. Next: prepare and release `bluetape4k-image 0.3.0`.
10. Sync `bluetape4k-dependencies` shared versions and managed catalog to the
    Maven Central-visible stable BOM versions.
11. Release `bluetape4k-dependencies 1.3.0`.
12. Start `bluetape4k-dependencies 1.3.1` only for
    `javers 0.3.0`, `text 0.3.0`, and `graph 0.6.0`.

## Verification Handles

Use these checks before changing this root queue again:

```bash
cd ~/work/bluetape4k
for repo in bluetape4k-projects bluetape4k-exposed bluetape4k-aws bluetape4k-image bluetape4k-text bluetape4k-graph bluetape4k-leader bluetape4k-javers bluetape4k-dependencies; do
  gh release list --repo "bluetape4k/$repo" --limit 1
  gh api "repos/bluetape4k/$repo/milestones?state=all&per_page=100" --jq '.[] | [.title,.state,.open_issues,.closed_issues,.number] | @tsv'
done

cd ~/work/bluetape4k/bluetape4k-dependencies
grep -E '^(baseVersion|snapshotVersion)=' gradle.properties
grep -E '^(bluetape4k-(bom|exposed-bom|aws-bom|image-bom|text-bom|graph-bom|leader-bom|javers-bom))[[:space:]]*=' gradle/libs.versions.toml
```
