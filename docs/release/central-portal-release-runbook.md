# bluetape4k Central Portal Release Runbook

This is the repeatable release procedure for independent `bluetape4k-*`
library repositories. It reflects the 2026-05-17 Central Portal release batch:
`projects 1.8.0`, `aws 0.1.0`, `text 0.1.0`, `graph 0.3.0`,
`javers 0.1.0`, `exposed 1.8.0`, `leader 0.1.0`, `image 0.1.0`, and
`dependencies 1.0.0`.

## Release Policy

- Keep `gradle.properties` stable:
  - `baseVersion=<release version>`
  - `snapshotVersion=`
- Publish snapshots by passing `-PsnapshotVersion=-SNAPSHOT`; do not edit
  `gradle.properties` just to publish a snapshot.
- Tag push is the release trigger. Tags must match `X.Y.Z`.
- `experimental`, `workshop`, examples, demos, and benchmarks are not release
  artifacts.
- `bluetape4k-dependencies` is released last, after every imported BOM is
  visible from Maven Central.
- Public release artifacts, PRs, issues, changelog entries, and commit messages
  are written in English.

## Repository Order

Use dependency order, not convenience order.

1. `bluetape4k-projects`
2. Repositories that depend only on `projects`, as applicable:
   `bluetape4k-aws`, `bluetape4k-text`, `bluetape4k-graph`,
   `bluetape4k-javers`
3. Repositories that depend on other released bluetape4k repos:
   `bluetape4k-exposed`, `bluetape4k-leader`, `bluetape4k-image`
4. `bluetape4k-dependencies`

For the 2026-05-17 batch, `bluetape4k-projects 1.8.0` was already released and
was not republished. `bluetape4k-image` waited until `bluetape4k-aws 0.1.0`
was visible from Maven Central. `bluetape4k-dependencies 1.0.0` waited until
all imported BOMs returned HTTP 200 from Maven Central.

## Preflight

Run this in each repository before tagging.

```bash
git switch develop
git pull --ff-only
git status --short --branch
grep -E '^(baseVersion|snapshotVersion)=' gradle.properties
rg 'SNAPSHOT' gradle/libs.versions.toml gradle.properties build.gradle.kts \
  --glob '!gradle.properties' \
  | grep -v 'snapshotVersion\|central-snapshot\|maven-snapshots\|# ' || true
gh pr list --state open
```

Expected:

- working tree clean
- local `develop` equals `origin/develop`
- `baseVersion` equals the tag to publish
- `snapshotVersion=` is empty
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
  generatePomFileForBluetapeVersionCatalogPublication \
  --no-daemon --no-configuration-cache --no-build-cache
rg -n 'SNAPSHOT|examples|demo|benchmark' \
  build/publications/BluetapeDependencies/pom-default.xml \
  build/publications/BluetapeVersionCatalog/pom-default.xml \
  gradle/libs.versions.toml build.gradle.kts
```

## Release PR

If preflight requires changes, create a PR first. Typical release-prep changes:

- version catalog references use released versions, not `-SNAPSHOT`
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

## Post-release

```bash
gh release view X.Y.Z --json tagName,publishedAt,url
git status --short --branch
```

Record:

- release workflow run ID
- GitHub Release URL
- Maven Central HTTP 200 evidence for representative artifacts
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
| GitHub Release fallback notes | no `CHANGELOG.md` section for the tag | Add release section before tagging or edit release notes after creation |
