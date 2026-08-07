# bluetape4k Central Portal Release Runbook

This is the repeatable release procedure for independent `bluetape4k-*`
library repositories. It reflects the 2026-05-17 Central Portal release batch:
`projects 1.8.0`, `aws 0.1.0`, `text 0.1.0`, `graph 0.3.0`,
`javers 0.1.0`, `exposed 1.8.0`, `leader 0.1.0`, `image 0.1.0`, and
`dependencies 1.0.0`.

## Release Flow Map

Use this map before choosing a command. Most release mistakes come from doing a
later phase while an earlier gate is still unresolved.

| Phase | Branch state | Version state | Required evidence | Next action |
|---|---|---|---|---|
| Normal development | `develop` | Own `baseVersion` is the next release; `snapshotVersion=`; internal bluetape4k refs use matching `-SNAPSHOT` | CI/Nightly acceptable, drift understood | Continue development or publish snapshots |
| Snapshot validation | `develop` | Same as normal development; snapshot suffix injected by workflow only | `publish-snapshot.yml` succeeds in dependency order | Start release prep only after required upstream snapshots are proven |
| Release prep | PR branch from `develop` | Own `baseVersion` equals release tag; `snapshotVersion=`; internal bluetape4k refs use released non-snapshot versions only after upstream HTTP 200 | pre-release checklist PASS, release workflow dry-run or diagnostic clean | Merge release-prep PR |
| Tag and release | `develop` at release-prep commit | Tag equals `baseVersion`; no checked-in snapshot suffix | GitHub release workflow succeeds, Central Portal accepts publication | Poll Maven Central until HTTP 200 |
| Post-release reopen | `develop` after release | Advance own `baseVersion` to next release; keep `snapshotVersion=`; restore development internal refs to matching `-SNAPSHOT` where needed | PR CI clean and snapshot train can run | Merge reopen PR, then publish snapshots |
| Final dependencies BOM | after imported BOMs are public | `bluetape4k-dependencies` imports released BOMs only | every imported BOM returns HTTP 200 from Maven Central | Release `bluetape4k-dependencies` last |

Stop if the current phase cannot satisfy its evidence. Do not compensate by
changing a downstream repository to an older released upstream version.

## Release Policy

- Follow `docs/governance/version-and-release-train.md` >
  `Version Management Policy` as the canonical version policy.
- Keep `gradle.properties` stable: `baseVersion=<next release version>` and
  `snapshotVersion=`.
- Publish snapshots by passing `-PsnapshotVersion=-SNAPSHOT` from
  `publish-snapshot.yml`.
- Publish releases with `baseVersion` only; `release.yml` must not inject
  `-SNAPSHOT`.
- Development branches reference internal `bluetape4k-*` dependencies with
  matching upstream `-SNAPSHOT` versions. Release-prep PRs remove the suffix only
  after the referenced upstream release is visible from Maven Central.
- Tag push is the release trigger. Tags must match `X.Y.Z`.
- `experimental`, `workshop`, examples, demos, and benchmarks are not release
  artifacts.
- `bluetape4k-dependencies` is released last, after every imported BOM is
  visible from Maven Central.
- Do not use the final `bluetape4k-dependencies` BOM version as the build-time
  Gradle catalog version for repositories that are part of the same release
  train. That creates a cycle: the final BOM cannot exist until those
  repositories are already released.
- Treat `bluetape4k-dependencies` as two different things with different
  distribution paths:
  - `bluetape4k-dependencies` is the final consumer BOM and uses semantic
    versions such as `1.1.3`.
  - `gradle/libs.versions.toml` is the internal build/contributor catalog for
    external library and plugin version alignment across `bluetape4k-*`
    repositories. Pin it by checking out the `bluetape4k-dependencies` repo at
    the release-train tag or commit; do not publish it as a Maven Central
    artifact.
- Public release artifacts, PRs, issues, changelog entries, release notes, and
  commit messages are written in Korean. Preserve code identifiers, URLs, exact
  errors, and machine-required tokens.

## BOM vs Catalog Roles

Keep these roles separate in every release decision.

`bluetape4k-dependencies` is a Maven BOM for users. It belongs in application
or workshop dependency declarations as a platform:

```kotlin
dependencies {
    implementation(platform("io.github.bluetape4k:bluetape4k-dependencies:1.1.3"))
    implementation("io.github.bluetape4k.leader:bluetape4k-leader-core")
}
```

The BOM participates in dependency resolution. If the user imports the BOM,
versionless `io.github.bluetape4k*` dependencies resolve to the BOM-managed
versions.

`bluetape4k-dependencies/gradle/libs.versions.toml` is a Gradle authoring
catalog for repository builds. It gives contributors centrally governed
external library and plugin versions such as `fory.kotlin`, Kotlin, Spring,
Ktor, Exposed, Testcontainers, and build plugins. It does not flow transitively
from the BOM and users do not need it when they use the BOM directly.

Do not use the catalog source ref as the release-version source for
`bluetape4k-*` to `bluetape4k-*` dependencies. Internal bluetape4k references
must point to the newly published upstream release version in dependency order.
That is why repository releases are ordered.

Repository builds must therefore read the catalog file from a checked-out
`bluetape4k-dependencies` repo for release-train validation:

```properties
bluetape4kDependenciesCatalogPath=../bluetape4k-dependencies/gradle/libs.versions.toml
bluetape4kDependenciesCatalogRef=catalog/2026-05-23-00
```

and import the catalog from that file:

```kotlin
val bluetape4kDependenciesCatalogFile = file(
    providers.gradleProperty("bluetape4kDependenciesCatalogPath")
        .orElse(providers.environmentVariable("BLUETAPE4K_DEPENDENCIES_CATALOG_PATH"))
        .orElse("../bluetape4k-dependencies/gradle/libs.versions.toml")
        .get(),
)

dependencyResolutionManagement {
    versionCatalogs {
        create("bt4k") {
            from(files(bluetape4kDependenciesCatalogFile))
        }
    }
}
```

Normal development and PR CI may fall back to the repo-local
`bluetape4k-dependencies` raw TOML from `develop`, but release validation must
pass an explicit checked-out path or `bluetape4kDependenciesCatalogRef` so the
train is pinned to an auditable source ref.

Do not name this property `bluetape4kDependenciesVersion`. That name is
reserved for the final user-facing BOM when a repository actually imports
`io.github.bluetape4k:bluetape4k-dependencies` as a platform.

### Catalog Source Ref Format

Use date-stamped tags or branch names for internal catalog source cuts:

```text
catalog/YYYY-MM-DD-NN
```

Examples:

- `catalog/2026-05-23-00`: first catalog source cut for the release train.
- `catalog/2026-05-23-02`: second catalog source cut after an upstream
  repository in the train has been released and later repositories need that
  new BOM.

The counter is per day and starts at `00`. Increment it only when publishing a
new immutable source ref. Do not rewrite a tag that release work has consumed.

Example: tag `bluetape4k-dependencies` as `catalog/2026-05-23-00`, check that
tag out in downstream release jobs, and verify their builds with
`bluetape4kDependenciesCatalogPath` pointing at that checkout. Cut a new
catalog tag only after the previous source cut proves the catalog shape.

### Release-Train Catalog Flow

For a multi-repository release train:

1. Audit every candidate repository from its last tag to `origin/develop`.
   Confirm open bug/blocker issues, open PRs, milestone state, and whether the
   post-tag changes belong in the next patch release.
2. Cut a build catalog source ref first if downstream repositories need new
   shared external library or plugin versions.
   Example: tag `bluetape4k-dependencies` as `catalog/2026-05-23-00`
   containing external versions such as `fory-kotlin:0.17.0`.
3. Update downstream release jobs or local builds to read
   `gradle/libs.versions.toml` from that checked-out `bluetape4k-dependencies`
   ref through `bluetape4kDependenciesCatalogPath`, then run the snapshot
   validation gate below before any downstream release tag is pushed.
4. If the catalog content changes during the train, cut a new
   `catalog/YYYY-MM-DD-NN` ref and update downstream jobs to that ref.
5. Release repositories in dependency order. If a later repository needs a BOM
   from an earlier repository in the same train, first publish the earlier
   repository, wait until its BOM is visible from Maven Central, then bump the
   later repository's local internal bluetape4k version reference. Do not use
   the catalog source ref as the internal bluetape4k release-version source.
6. After all imported BOMs are visible from Maven Central, release the final
   `bluetape4k-dependencies` BOM. This release publishes the user-facing BOM;
   it does not publish the internal build catalog.
7. Verify user-facing downstream builds with the final
   `bluetape4k-dependencies` BOM and versionless `io.github.bluetape4k*`
   dependencies.

This flow prevents the common cycle:

```text
repo A needs final dependencies BOM
final dependencies BOM needs repo A release
```

The catalog can centralize external dependency versions and lead downstream
build migration, but it must not replace repository release order. For
`bluetape4k-*` to `bluetape4k-*` dependencies, the referenced upstream release
version must be set as the newly published release version and publicly
resolvable. The final BOM closes the train.

## Repository Order

Use dependency order, not convenience order.

1. `bluetape4k-projects`
2. Repositories that depend only on `projects`, as applicable:
   `bluetape4k-exposed`, `bluetape4k-text`, `bluetape4k-graph`,
   `bluetape4k-javers`
3. Repositories that depend on released `exposed` or other bluetape4k repos:
   `bluetape4k-aws`, `bluetape4k-leader`
4. Repositories that depend on released `aws`:
   `bluetape4k-image`
5. `bluetape4k-dependencies`

This list is a default, not a shortcut. Recompute the repository dependency
graph for every release train from current `settings.gradle.kts`,
`gradle/libs.versions.toml`, and all `build.gradle.kts` files before accepting
the order. If `bluetape4k-javers` adds a `javers-exposed` module or any
`io.github.bluetape4k.exposed` reference, move `javers` behind the target
`bluetape4k-exposed` release and wait for that exposed version to return Maven
Central HTTP 200.

For the 2026-05-17 batch, `bluetape4k-projects 1.8.0` was already released and
was not republished. `bluetape4k-image` waited until `bluetape4k-aws 0.1.0`
was visible from Maven Central. `bluetape4k-dependencies 1.0.0` waited until
all imported BOMs returned HTTP 200 from Maven Central.

## Internal Reference Preflight

Before preparing each repository in the order above, inspect every
`io.github.bluetape4k*` version that repository references. On `develop`, those
internal references normally point at the matching upstream `-SNAPSHOT` line.
In the release-prep branch, remove `-SNAPSHOT` only for upstream repositories
that have already been released and return HTTP 200 from Maven Central.

If the referenced upstream repository is part of the same release train, wait
for that upstream target version to be released and publicly resolvable before
preparing or releasing the downstream repository. Do not fall back to the
previous public release just because it is the latest version currently
available. Before the upstream release is available, downstream development
branches keep using the matching upstream `-SNAPSHOT` reference.

If the referenced upstream repository is not part of the release train, use the
latest public upstream release version and verify it from Maven Central.

This check is separate from `bluetape4kDependenciesCatalogPath`. The shared
catalog is for external library/plugin version alignment; internal bluetape4k
release versions follow repository release order.

Typical checks:

```bash
rg -n 'bluetape4k(-[a-z]+)? = "|bluetape4k-.*-bom = "|io\.github\.bluetape4k' \
  gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts

rg -n 'exposed|bluetape4k-exposed|io\.github\.bluetape4k\.exposed|bluetape4k\.exposed' \
  settings.gradle.kts gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts

curl -s -o /dev/null -w "%{http_code}" \
  "https://repo.maven.apache.org/maven2/io/github/bluetape4k/bluetape4k-bom/<version>/bluetape4k-bom-<version>.pom"

curl -s -o /dev/null -w "%{http_code}" \
  "https://repo.maven.apache.org/maven2/io/github/bluetape4k/aws/bluetape4k-aws-bom/<version>/bluetape4k-aws-bom-<version>.pom"

curl -s -o /dev/null -w "%{http_code}" \
  "https://repo.maven.apache.org/maven2/io/github/bluetape4k/exposed/bluetape4k-exposed-bom/<version>/bluetape4k-exposed-bom-<version>.pom"
```

Expected:

- `bluetape4k-projects` target version is released and visible before
  exposed/text/graph/javers, aws, leader, or image removes `-SNAPSHOT` from its
  reference.
- If aws references exposed modules and exposed is in the train, release and
  verify the exposed target version first, then bump aws's exposed reference.
- If javers references exposed modules, for example a future `javers-exposed`
  module, release and verify the exposed target version first, then bump
  javers's exposed reference.
- If image references aws and aws is in the train, release and verify the aws
  target version first, then bump image's aws reference.
- If leader or another repo references exposed artifacts and exposed is in the
  train, release and verify the exposed target version first.
- `bluetape4k-dependencies` is not used to shortcut library release order; it
  is released last after all imported BOMs are visible.

## Preflight

Run this in each repository before tagging.

```bash
git switch develop
git pull --ff-only
git status --short --branch
grep -E '^(baseVersion|snapshotVersion)=' gradle.properties
grep -E '^bluetape4kDependenciesCatalogPath=' gradle.properties || true
rg 'SNAPSHOT' gradle/libs.versions.toml gradle.properties build.gradle.kts \
  --glob '!gradle.properties' \
  | grep -v 'snapshotVersion\|central-snapshot\|maven-snapshots\|# ' || true
gh pr list --state open
gh api "repos/bluetape4k/$(basename "$PWD")/milestones?state=open&per_page=100" \
  --jq '.[] | [.title,.open_issues,.closed_issues] | @tsv'
gh issue list --state open --milestone "<target-version>" --limit 100
rg -n 'bluetape4k(-[a-z]+)? = "|bluetape4k-.*-bom = "|io\.github\.bluetape4k' \
  gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts
```

Expected:

- working tree clean
- local `develop` equals `origin/develop`
- `baseVersion` equals the tag to publish
- `snapshotVersion=` is empty
- GitHub has a milestone whose title exactly matches the target version
- every open issue in the target milestone is either resolved before release or
  explicitly deferred out of that milestone
- non-target open milestones/backlog issues are reviewed so feature work is not
  silently pulled into a patch release
- every `bluetape4k-*` version referenced by the local repository build is the
  intended upstream target release and returns HTTP 200 from Maven Central; if
  that upstream target is not yet published, stop and wait instead of using the
  previous release
- if the repository imports the shared build catalog, it reads
  `bluetape4k-dependencies/gradle/libs.versions.toml` through
  `bluetape4kDependenciesCatalogPath` or
  `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH`, not a Maven-published catalog
  artifact
- no unreleased `*-SNAPSHOT` bluetape4k dependency references
- release-blocking PRs are merged

## BOM And Publication Guards

Before publishing a repo BOM, verify the build excludes non-library modules
from all release metadata paths.

Exclude these from BOM constraints, NMCP aggregation, publication/signing setup,
and generated ecosystem BOM entries:

- `examples/`
- `*-examples`
- `*-demo`
- `benchmark/`
- `*-benchmark`

Known traps:

- Nested Gradle includes create both `:examples` and `:examples:*`. Filter both.
- Filtering only NMCP aggregation is not enough. If a non-library module still
  has `maven-publish`, Gradle can generate a publication and Central validation
  can see it.
- Do not disable Spring dependency-management POM customization for release
  artifacts. `generatedPomCustomization { setEnabled(false) }` can produce POMs
  with missing dependency version metadata and fail Central validation.
- `bluetape4k-dependencies` generated sections must be regenerated with
  `scripts/sync-managed-catalog.py`; do not hand-edit generated managed-module
  blocks.

Verification commands:

```bash
# repo-specific publication name examples:
./gradlew clean generatePomFileForBluetapeAwsPublication --no-daemon --no-configuration-cache --no-build-cache
./gradlew clean generatePomFileForBluetapeExposedPublication --no-daemon --no-configuration-cache --no-build-cache
./gradlew clean generatePomFileForBluetapeGraphPublication --no-daemon --no-configuration-cache --no-build-cache
./gradlew clean generatePomFileForBluetapeImagePublication --no-daemon --no-configuration-cache --no-build-cache
./gradlew clean generatePomFileForBluetapeLeaderPublication --no-daemon --no-configuration-cache --no-build-cache

# generated POM scan should print nothing
rg -n 'SNAPSHOT|examples|demo|benchmark' build/publications
```

For `bluetape4k-dependencies`:

```bash
python3 -m unittest tests/test_sync_managed_catalog.py
scripts/sync-managed-catalog.py --write --check --summary
./gradlew generatePomFileForBluetapeDependenciesPublication \
  --no-daemon --no-configuration-cache --no-build-cache
rg -n 'SNAPSHOT|examples|demo|benchmark' \
  build/publications/BluetapeDependencies/pom-default.xml \
  gradle/libs.versions.toml build.gradle.kts
```

## Snapshot Validation Gate

Run this gate before any real release publish or release tag push when the
train changes shared catalog aliases, upstream BOM coordinates, or centrally
governed dependency versions.

Snapshot validation proves catalog mechanics and downstream compatibility. It
does not allow a downstream release to depend on an upstream `bluetape4k-*`
version that has not been released yet. For release candidates, internal
`bluetape4k-*` dependency versions are still governed by repository release
order, not by the catalog source ref.

1. In `bluetape4k-dependencies`, commit the shared catalog changes and create
   an immutable source ref for the train:

   ```bash
   git tag catalog/YYYY-MM-DD-NN
   ```

2. In each downstream repository, check out `bluetape4k-dependencies` at that
   ref and point Gradle at the checked-out TOML:

   ```bash
   export BLUETAPE4K_DEPENDENCIES_CATALOG_PATH="$WORKSPACE/bluetape4k-dependencies/gradle/libs.versions.toml"
   ```

   GitHub Actions should use a second checkout of `bluetape4k-dependencies`
   with `ref: catalog/YYYY-MM-DD-NN` and set the same environment variable or
   pass `-Pbluetape4kDependenciesCatalogPath=...`.

3. Verify each affected repository resolves the checked-out catalog, without
   `mavenLocal()`:

   ```bash
   ./gradlew help --refresh-dependencies \
     --no-daemon --no-configuration-cache --no-build-cache
   ```

   For a cross-repository smoke check:

   ```bash
   for repo in \
     bluetape4k-projects bluetape4k-aws bluetape4k-text bluetape4k-graph \
     bluetape4k-javers bluetape4k-exposed bluetape4k-leader bluetape4k-image
   do
     export BLUETAPE4K_DEPENDENCIES_CATALOG_PATH="$PWD/bluetape4k-dependencies/gradle/libs.versions.toml"
     (cd "$repo" && ./gradlew help --refresh-dependencies \
       --no-daemon --no-configuration-cache --no-build-cache)
   done
   ```

4. Run targeted compile/tests for repositories whose release content changed.
   `help` only proves settings/catalog resolution; it does not prove runtime or
   API compatibility.

   Before accepting a downstream test result as release evidence, verify every
   internal upstream coordinate it resolved is a public release:

   ```bash
   curl -s -o /dev/null -w "%{http_code}" \
     "https://repo.maven.apache.org/maven2/io/github/bluetape4k/bluetape4k-bom/<version>/bluetape4k-bom-<version>.pom"
   ```

Do not push release tags or publish release artifacts while downstream
repositories still require an unpublished upstream release or an uncaptured
catalog source change.

## Post-release Snapshot Publish Train

Run this train after release and post-release reopen PRs have advanced
`baseVersion` to the next release line. This is the development-line validation
gate: internal `bluetape4k-*` references should use matching `-SNAPSHOT`
versions, and checked-in `snapshotVersion` should remain empty.

Use dependency order and stop on the first failure:

1. `bluetape4k-projects`
2. `bluetape4k-exposed`, `bluetape4k-text`, `bluetape4k-graph`,
   `bluetape4k-javers`
3. `bluetape4k-aws`, `bluetape4k-leader`
4. `bluetape4k-image`
5. `bluetape4k-dependencies`

For each repository:

```bash
git switch develop
git pull --ff-only
grep -E '^(baseVersion|snapshotVersion)=' gradle.properties
rg -n 'bluetape4k(-[a-z]+)? = "|bluetape4k-.*-bom = "|io\.github\.bluetape4k' \
  gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts
gh workflow run publish-snapshot.yml --ref develop
gh run list --workflow publish-snapshot.yml --branch develop --limit 1
```

Do not assume `publish-snapshot.yml` accepts the same inputs in every
repository. If a repo has no `diagnoseSigning` input, dispatch it without
`--field diagnoseSigning=false`.

After each successful publish, verify snapshot metadata from the snapshot
repository, not from release Maven Central POM URLs:

```bash
curl -fsSL \
  "https://central.sonatype.com/repository/maven-snapshots/<group-path>/<artifact>/<version>-SNAPSHOT/maven-metadata.xml" \
  | rg '<lastUpdated>|<timestamp>|<buildNumber>'
```

For `bluetape4k-dependencies`, its CI and local verification must use snapshot
metadata checks while the catalog imports `-SNAPSHOT` BOMs:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
scripts/verify-managed-artifacts.py --summary --allow-snapshots
```

Release-prep branches must switch back to strict release verification: remove
internal `-SNAPSHOT` references only after every referenced upstream release is
publicly visible from Maven Central.

## Release PR

If preflight requires changes, create a PR first. Typical release-prep changes:

- version catalog references use released versions, not `-SNAPSHOT`; do this
  only after the referenced upstream release is visible from Maven Central
- `baseVersion` already equals the tag that will be pushed; if this is a
  post-release reopen PR instead, advance `baseVersion` to the next release
  version and keep `snapshotVersion=` empty
- BOM artifact/version keys are consistent, for example `bluetape4k-bom` and
  `bluetape4k-exposed-bom`
- non-library module filters are present
- `CHANGELOG.md` has a release section for the tag
- a concise lesson records release-specific decisions:
  use repo-local `docs/lessons/YYYY-MM-DD-*.md` for repo-specific behavior, or
  `.github/docs/lessons/YYYY-MM-DD-*.md` for organization-wide release process
  behavior

Use rebase merge by default for release-prep PRs.

```bash
git switch -c chore/release-prep-X.Y.Z
git add <files>
git commit -m $'<intent line>\n\n<body>\n\nConstraint: ...\nConfidence: high\nScope-risk: narrow\nDirective: ...\nTested: ...\nNot-tested: ...'
git push -u origin chore/release-prep-X.Y.Z
gh pr create --base develop --head chore/release-prep-X.Y.Z --assignee debop
gh pr view <PR> --json mergeStateStatus,statusCheckRollup
gh pr merge <PR> --rebase --delete-branch
git switch develop
git pull --ff-only
```

## Tag And Release

```bash
git tag -a X.Y.Z -m "Release X.Y.Z"
git push origin X.Y.Z
sleep 5
gh run list --workflow release.yml --limit 3 \
  --json databaseId,status,conclusion,headBranch,headSha,createdAt,event
```

Monitor the run:

```bash
gh run watch <RUN_ID> --interval 20 --exit-status
```

Expected jobs:

1. `Resolve release version`
2. `Publish RELEASE to Maven Central Portal`
3. `Create GitHub Release`

All jobs must succeed.

## Central Portal And Maven Central Verification

The workflow can succeed before artifacts are visible from the public Maven
Central repository. Treat GitHub Actions success as "Central Portal accepted";
treat Maven Central HTTP 200 as "consumers can resolve it."

Poll Maven Central:

```bash
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://repo.maven.apache.org/maven2/<group-path>/<artifact>/<version>/<artifact>-<version>.pom")
  echo "$code <artifact>"
  [ "$code" = "200" ] && break
  sleep 20
done
```

Do not use `path` as a loop variable in `zsh`; it aliases `PATH` and can break
commands inside the shell. Use `artifact_path` or another name.

## Failed Release Recovery

If Central validation fails after a tag push:

1. Read the failing job logs.
2. Fix the repository on a normal PR branch.
3. Wait for PR CI to become clean.
4. Merge to `develop`.
5. Fast-forward local `develop`.
6. Rewrite the failed tag to the fixed commit with `--force-with-lease`.

```bash
git switch develop
git pull --ff-only
git fetch origin --tags --force
old_tag=$(git rev-parse refs/tags/X.Y.Z)
git tag -fa X.Y.Z -m "Release X.Y.Z"
git push --force-with-lease=refs/tags/X.Y.Z:$old_tag origin refs/tags/X.Y.Z
```

Only rewrite a tag for a failed or unusable release. Do not rewrite a tag that
has already been successfully consumed without an explicit release decision.

## `bluetape4k-dependencies` Final Release

Before tagging `bluetape4k-dependencies`, verify every imported BOM is visible
from Maven Central.

```bash
for artifact_path in \
  io/github/bluetape4k/bluetape4k-bom/1.8.0/bluetape4k-bom-1.8.0.pom \
  io/github/bluetape4k/aws/bluetape4k-aws-bom/0.1.0/bluetape4k-aws-bom-0.1.0.pom \
  io/github/bluetape4k/image/bluetape4k-image-bom/0.1.0/bluetape4k-image-bom-0.1.0.pom \
  io/github/bluetape4k/text/bluetape4k-text-bom/0.1.0/bluetape4k-text-bom-0.1.0.pom \
  io/github/bluetape4k/graph/bluetape4k-graph-bom/0.3.0/bluetape4k-graph-bom-0.3.0.pom \
  io/github/bluetape4k/leader/bluetape4k-leader-bom/0.1.0/bluetape4k-leader-bom-0.1.0.pom \
  io/github/bluetape4k/exposed/bluetape4k-exposed-bom/1.8.0/bluetape4k-exposed-bom-1.8.0.pom \
  io/github/bluetape4k/javers/bluetape4k-javers-bom/0.1.0/bluetape4k-javers-bom-0.1.0.pom
do
  curl -s -o /dev/null -w "%{http_code} $artifact_path\n" \
    "https://repo.maven.apache.org/maven2/$artifact_path"
done
```

Only tag `bluetape4k-dependencies` after all lines return `200`.

The final `bluetape4k-dependencies` release workflow publishes only the
`BluetapeDependencies` publication. The internal Gradle catalog is consumed from
the `bluetape4k-dependencies` git ref and is not a Maven Central publication.

## Website Documentation Refresh

After the final release artifacts are visible from Maven Central, update
`bluetape4k.github.io` in the same release train. The website is the public
entrypoint for current dependency coordinates, so it must not lag behind the
published BOMs.

Update at least these pages in both English and Korean when the released
versions change:

- `src/content/docs/getting-started.mdx`
- `src/content/docs/ko/getting-started.mdx`
- `src/content/docs/ecosystem/version-governance.mdx`
- `src/content/docs/ko/ecosystem/version-governance.mdx`
- `src/content/docs/ecosystem/repositories.mdx`
- `src/content/docs/ko/ecosystem/repositories.mdx`

Verification:

```bash
cd ../bluetape4k.github.io
npm run build
git diff --check
```

After merging the website PR, verify the GitHub Pages deployment and live page:

```bash
gh run list --workflow="Deploy Website" --limit 3 \
  --json databaseId,status,conclusion,headBranch,headSha,createdAt
curl -fsSL https://bluetape4k.github.io/ecosystem/version-governance/ \
  | rg 'bluetape4k-dependencies|bluetape4k-bom|bluetape4k-.*-bom'
```

Record the website PR, deploy run URL, and live-page evidence in the release
notes or release lesson.

## Post-release

```bash
gh release view X.Y.Z --json tagName,publishedAt,url
git status --short --branch
```

Record:

- release workflow run ID
- GitHub Release URL
- Maven Central HTTP 200 evidence for representative artifacts
- post-release reopen PR when the repository continues on `develop`:
  `baseVersion` advanced to the next release, `snapshotVersion=` remains empty,
  and internal bluetape4k references return to matching `-SNAPSHOT` where
  development should consume snapshots
- snapshot workflow run ID after the reopen PR when downstream development needs
  the new snapshot
- dependency-order snapshot train evidence: PR URLs, publish run IDs, and
  snapshot `maven-metadata.xml` timestamps for every upstream BOM consumed by a
  downstream repo
- `bluetape4k.github.io` PR and GitHub Pages deployment evidence
- any Central validation failures and recovery PRs

## Common Failures

| Symptom | Cause | Fix |
|---|---|---|
| Central validation reports missing dependency versions | Spring dependency-management generated POM customization disabled | Remove `generatedPomCustomization { setEnabled(false) }` for published modules and regenerate POMs |
| Central validation includes `examples@<version>` | `:examples` parent project was not excluded | Filter both `path == ":examples"` and `path.startsWith(":examples:")` |
| BOM includes benchmark aliases | generator or BOM constraints only excluded examples | Exclude `benchmark/` and `*-benchmark`, regenerate `bluetape4k-dependencies` |
| Release workflow succeeds but Maven Central returns 404 | Central Portal accepted, public repository has not propagated | Poll `repo.maven.apache.org` until HTTP 200 |
| Tag push points to wrong commit after a failed release | fix PR merged after tag was created | Retag with `--force-with-lease=refs/tags/X.Y.Z:<old-tag>` |
| `zsh: command not found: curl` inside polling loop | loop variable named `path` overwrote zsh `PATH` | Rename loop variable to `artifact_path` |
| `gh workflow run publish-snapshot.yml --field diagnoseSigning=false` returns HTTP 422 | repository workflow has no `diagnoseSigning` input | Dispatch without the field after checking the workflow inputs |
| Snapshot artifact verification returns 404 from `repo1.maven.org` or a timestamped POM URL | snapshots are stored under Central snapshot metadata, not release Maven Central POM paths | Check `https://central.sonatype.com/repository/maven-snapshots/.../maven-metadata.xml` |
| `bluetape4k-dependencies` CI rejects `-SNAPSHOT` managed artifacts after post-release reopen | release artifact verifier is running in strict release mode on a development snapshot line | Use `--allow-snapshots` for develop/normal PRs and keep strict mode for main-target release PRs |
| GitHub Release fallback notes | no `CHANGELOG.md` section for the tag | Add release section before tagging or edit release notes after creation |
