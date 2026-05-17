# bluetape4k Release Guide

Complete release reference for the bluetape4k organization.
Covers dependency order, pre-release validation, step-by-step procedure, and post-release tasks.

Validated against `bluetape4k-projects` 1.8.0 release (2026-05-17).

---

## Contents

1. [Repository Dependency & Release Order](#1-repository-dependency--release-order)
2. [Pre-release Checklist](#2-pre-release-checklist)
3. [Release Procedure (Steps 1–13)](#3-release-procedure-steps-113)
4. [Monitoring the Release Workflow](#4-monitoring-the-release-workflow)
5. [Post-release Tasks](#5-post-release-tasks)
6. [Common Pitfalls](#6-common-pitfalls)

---

## 1. Repository Dependency & Release Order

### Dependency Graph

```
bluetape4k-projects (io.github.bluetape4k)
│
├── bluetape4k-exposed   ──────────────────────────────────┐
│   (io.github.bluetape4k.exposed)                        │
│                                                          │
├── bluetape4k-aws                                         │
│   (io.github.bluetape4k.aws)                             │
│                                                          ▼
├── bluetape4k-image                            bluetape4k-leader
│   (io.github.bluetape4k.image)                (io.github.bluetape4k.leader)
│
├── bluetape4k-text
│   (io.github.bluetape4k.text)
│
├── bluetape4k-graph
│   (io.github.bluetape4k.graph)
│
└── bluetape4k-javers
    (io.github.bluetape4k.javers)

All libraries above ──────────────────────────────────────►  bluetape4k-dependencies
                                                             (io.github.bluetape4k)
                                                             [version catalog aggregator]
```

**Notes:**
- `bluetape4k-graph` uses `org.jetbrains.exposed` (upstream) directly — does **not** depend on `bluetape4k-exposed`.
- `bluetape4k-leader` depends on `bluetape4k-exposed` (test helpers: `exposed-jdbc-tests`, `exposed-r2dbc-tests`).
- All repos depend on `bluetape4k-projects` as the foundational BOM.
- `bluetape4k-dependencies` is the ecosystem-wide version catalog; release it last.

### Release Tiers

| Tier | Repository | Group ID | Notes |
|---|---|---|---|
| **0** | `bluetape4k-projects` | `io.github.bluetape4k` | Foundation BOM — release first |
| **1** | `bluetape4k-exposed` | `io.github.bluetape4k.exposed` | Independent of other Tier 1 repos |
| **1** | `bluetape4k-aws` | `io.github.bluetape4k.aws` | Independent of other Tier 1 repos |
| **1** | `bluetape4k-image` | `io.github.bluetape4k.image` | Independent of other Tier 1 repos |
| **1** | `bluetape4k-text` | `io.github.bluetape4k.text` | Independent of other Tier 1 repos |
| **1** | `bluetape4k-graph` | `io.github.bluetape4k.graph` | Uses JetBrains Exposed directly, not bluetape4k-exposed |
| **1** | `bluetape4k-javers` | `io.github.bluetape4k.javers` | Independent of other Tier 1 repos |
| **2** | `bluetape4k-leader` | `io.github.bluetape4k.leader` | Blocked on `bluetape4k-exposed` |
| **3** | `bluetape4k-dependencies` | `io.github.bluetape4k` | Aggregator catalog — always last |

Tier 1 repos have **no cross-dependencies** and can be released in parallel.

### Release Sequence Diagram

```
Step 1:  [released] bluetape4k-projects 1.8.0
                          │
Step 2:  ┌────────────────┼────────────────┬────────────┬────────────────┐
         ▼                ▼                ▼            ▼                ▼
     bluetape4k-   bluetape4k-aws  bluetape4k-  bluetape4k-  bluetape4k-javers
       exposed          0.1.0        image        text           0.1.0
        1.8.0                        0.1.0        0.1.0
                                                              + bluetape4k-graph
                                                                   0.3.0
         │
Step 3:  ▼
     bluetape4k-leader
          0.1.0
              │
Step 4:       ▼
     bluetape4k-dependencies
          1.0.0
```

### Verify Dependency Before Releasing

```bash
# Must return 200 before proceeding with any downstream release
curl -o /dev/null -s -w "%{http_code}" \
  "https://repo1.maven.org/maven2/<group-path>/<artifact>/<version>/<artifact>-<version>.pom"

# Example: verify bluetape4k-exposed 1.8.0
curl -o /dev/null -s -w "%{http_code}" \
  "https://repo1.maven.org/maven2/io/github/bluetape4k/exposed/exposed-bom/1.8.0/exposed-bom-1.8.0.pom"
```

### Current Status

Update this table after each release.

| Repository | Target Version | Maven Central | Status |
|---|---|---|---|
| `bluetape4k-projects` | 1.8.0 | ✅ 1.8.0 | Released |
| `bluetape4k-exposed` | 1.8.0 | ❌ unreleased | In progress |
| `bluetape4k-graph` | 0.3.0 | ❌ 0.2.0 released | Prepared (snapshotVersion cleared) |
| `bluetape4k-aws` | 0.1.0 | ❌ unreleased | Queued |
| `bluetape4k-image` | 0.1.0 | ❌ unreleased | Queued |
| `bluetape4k-text` | 0.1.0 | ❌ unreleased | Queued |
| `bluetape4k-javers` | 0.1.0 | ❌ unreleased | Queued |
| `bluetape4k-leader` | 0.1.0 | ❌ unreleased | Blocked on bluetape4k-exposed |
| `bluetape4k-dependencies` | 1.0.0 | ❌ unreleased | Blocked on Tier 1/2 |

---

## 2. Pre-release Checklist

Run this checklist **for each repository** before triggering the release workflow.

### Quick Scan Script

```bash
#!/usr/bin/env bash
# Run from the target repository root

echo "=== 1. SNAPSHOT dependencies ==="
rg "SNAPSHOT" gradle/libs.versions.toml 2>/dev/null | grep -v "snapshotVersion\|central-snapshot\|maven-snapshots\|# "

echo "=== 2. Open bug issues ==="
gh issue list --state open --label "bug" --limit 10 2>/dev/null

echo "=== 3. Open PRs ==="
gh pr list --state open 2>/dev/null

echo "=== 4. CHANGELOG ==="
head -15 CHANGELOG.md

echo "=== 5. Nightly CI (last 3) ==="
gh run list --workflow="Nightly" --limit 3 2>/dev/null

echo "=== 6. gradle.properties ==="
grep "baseVersion\|snapshotVersion" gradle.properties

echo "=== 7. develop branch state ==="
git log --oneline origin/develop..HEAD
git status --porcelain
git worktree list
```

### 1. Dependency Versions

```bash
# Check for SNAPSHOT references
rg "SNAPSHOT" gradle/libs.versions.toml gradle.properties build.gradle.kts \
  --glob "!gradle.properties" | grep -v "snapshotVersion\|central-snapshot\|maven-snapshots\|# "
```

- [ ] All `bluetape4k-*` versions in `gradle/libs.versions.toml` are release versions (no `-SNAPSHOT`)
- [ ] `io.github.bluetape4k` and `io.github.bluetape4k.exposed` use **separate version keys** in the catalog (different release cycles)
- [ ] Each version actually exists on Maven Central (HTTP 200)
- [ ] No external library SNAPSHOT references (`-SNAPSHOT`, `.BUILD-SNAPSHOT`)
- [ ] `exposed`, `spring-boot`, `kotlin`, `kotlinx-coroutines` are GA versions

> ⚠️ **Trap**: same version number ≠ same release. `bluetape4k-projects 1.8.0` and `bluetape4k-exposed 1.8.0` are independent artifacts released separately. Each must be HTTP 200 on Maven Central independently.

### 2. Code Quality

```bash
gh issue list --state open --label "bug" --limit 20
gh pr list --state open
```

- [ ] **bug** label open issues = 0 (or deferred to next version)
- [ ] **blocker** / **critical** label open issues = 0
- [ ] No open PRs blocking the release (release-related fix/chore PRs merged)
- [ ] New or changed public APIs have English KDoc
- [ ] `README.md` and locale README files updated

### 3. CHANGELOG

```bash
head -30 CHANGELOG.md
```

- [ ] `## [X.Y.Z] — Unreleased` → `## [X.Y.Z] — YYYY-MM-DD` date stamped
- [ ] `## [Unreleased]` section is empty or separated into next version
- [ ] Major changes recorded (Added / Changed / Fixed / Removed)

### 4. CI / Tests

```bash
gh run list --workflow="Nightly" --limit 5
```

- [ ] Last **3 Nightly runs: SUCCESS**
- [ ] Last Nightly ran within **48 hours**
- [ ] `develop` branch = `origin/develop` (no local ahead/behind)
- [ ] No uncommitted changes: `git status --porcelain`
- [ ] No leftover worktrees: `git worktree list`

### 5. Version Files

```bash
grep "baseVersion\|snapshotVersion" gradle.properties
```

- [ ] `baseVersion=X.Y.Z` matches the release version
- [ ] `snapshotVersion=-SNAPSHOT` (will be cleared on the release branch)

### 6. Release Workflow

```bash
grep -A5 "on:" .github/workflows/release.yml | head -15
```

- [ ] `release.yml` exists and triggers on tag pattern `[0-9]+.[0-9]+.[0-9]+`
- [ ] Snapshot and release workflows are separate
- [ ] NMCP / Maven Central Portal credentials are configured (confirm via prior successful release)

### 7. Release Dependency Order

- [ ] All lower-tier repos are already released on Maven Central (HTTP 200)
- [ ] Their versions are referenced as release versions (not `-SNAPSHOT`) in this repo's catalog

---

## 3. Release Procedure (Steps 1–13)

### Prerequisites

- `develop` branch is green (Nightly CI all SUCCESS)
- All hard-blocker issues closed
- CHANGELOG `## [X.Y.Z] — Unreleased` section complete
- `gradle.properties`: `baseVersion=X.Y.Z`, `snapshotVersion=-SNAPSHOT`

---

### Step 1 — Pre-release cleanup

Remove stale/unused version properties before cutting a release branch.

```bash
# Check for unused version properties
rg "Version=" gradle.properties
rg "val \w+Version: String by project" build.gradle.kts

# Verify nothing references each property in submodules
rg "<property>" --include="*.kts" | grep -v "build.gradle.kts"
```

Remove any properties with zero submodule references.

---

### Step 2 — Create release branch (in worktree)

```bash
git worktree add .worktrees/release/X.Y.Z -b release/X.Y.Z
```

---

### Step 3 — Edit release prep files

**`gradle.properties`**

```diff
-snapshotVersion=-SNAPSHOT
+snapshotVersion=
```

Also remove unused `*Version` properties found in Step 1.

**`build.gradle.kts`**

Remove `val <property>: String by project` declarations for removed properties.

**`CHANGELOG.md`**

```diff
-## [X.Y.Z] — Unreleased
+## [X.Y.Z] — YYYY-MM-DD
```

---

### Step 4 — Commit, push, create PR

```bash
cd .worktrees/release/X.Y.Z
git add gradle.properties build.gradle.kts CHANGELOG.md
git commit -m "chore: prepare X.Y.Z release — clear snapshotVersion, stamp CHANGELOG date"
git push -u origin release/X.Y.Z

gh pr create \
  --base develop \
  --head release/X.Y.Z \
  --title "chore: prepare X.Y.Z release" \
  --body "..."
```

---

### Step 5 — Wait for CI and merge

```bash
# Poll until all checks complete
gh pr view <PR#> --json statusCheckRollup \
  --jq '[.statusCheckRollup[]] | {total:length, done:[.[]|select(.status=="COMPLETED")]|length, failed:[.[]|select(.conclusion=="failure")]|length}'

# Merge when done=total and failed=0
gh pr merge <PR#> --squash --delete-branch
```

> If `develop` is checked out in the main worktree, `--delete-branch` may fail locally. Verify with `gh pr view <PR#> --json state`.

---

### Step 6 — Sync local develop

```bash
git fetch origin develop
git merge --ff-only origin/develop
git log --oneline -3
```

Verify `snapshotVersion=` is empty and `baseVersion=X.Y.Z`:

```bash
grep "baseVersion\|snapshotVersion" gradle.properties
# Expected:
# baseVersion=X.Y.Z
# snapshotVersion=
```

---

### Step 7 — Tag and push → triggers Publish Release workflow

The `release.yml` workflow fires on any tag matching `[0-9]+.[0-9]+.[0-9]+`.

```bash
git tag -a X.Y.Z -m "Release X.Y.Z"
git push origin X.Y.Z

sleep 5
gh run list --workflow="release.yml" --limit 3
```

---

### Step 8 — Monitor Publish Release workflow

```bash
gh run view <RUN_ID> --json status,conclusion,jobs \
  --jq '{status:.status, conclusion:.conclusion, jobs:[.jobs[]|{name:.name,status:.status,conclusion:.conclusion}]}'
```

Expected jobs (all must reach `conclusion: success`):

1. `Resolve release version` — validates tag format and `gradle.properties` match
2. `Publish RELEASE to Maven Central Portal` — runs `publishAggregationToCentralPortal`
3. `Create GitHub Release` — reads `CHANGELOG.md` section, generates release notes

---

### Step 9 — Verify GitHub Release

```bash
gh release view X.Y.Z --json tagName,publishedAt,url
```

---

### Step 10 — Update release notes (bilingual)

```bash
gh release edit X.Y.Z --notes-file /path/to/release-notes-bilingual.md
```

**File structure:**

```markdown
<details open>
<summary>English</summary>

### Added
...

### Fixed
...

</details>

---

<details>
<summary>한국어</summary>

### Added (추가)
...

</details>

---

## Contributors
...

**Full Changelog**: https://github.com/bluetape4k/<repo>/compare/PREV...X.Y.Z
```

- `<details open>` = English (default expanded)
- `<details>` = Korean (default collapsed)

---

### Step 11 — Update `bluetape4k-dependencies`

```bash
cd ~/work/bluetape4k/bluetape4k-dependencies
git worktree add .worktrees/chore/bump-<repo>-X.Y.Z -b chore/bump-<repo>-X.Y.Z

# Edit gradle/libs.versions.toml
# <repo-version-key> = "X.Y.Z-SNAPSHOT"  →  "X.Y.Z"

git add gradle/libs.versions.toml
git commit -m "chore: bump <repo> X.Y.Z-SNAPSHOT → X.Y.Z"
git push -u origin chore/bump-<repo>-X.Y.Z

gh pr create \
  --repo bluetape4k/bluetape4k-dependencies \
  --base develop \
  --head chore/bump-<repo>-X.Y.Z \
  --title "chore: bump <repo> X.Y.Z-SNAPSHOT → X.Y.Z"
```

Wait for CI and merge:

```bash
gh pr view <PR#> --repo bluetape4k/bluetape4k-dependencies \
  --json statusCheckRollup --jq '...'

gh pr merge <PR#> --repo bluetape4k/bluetape4k-dependencies --squash --delete-branch
```

---

### Step 12 — Bump to next SNAPSHOT in source repo

```bash
cd ~/work/bluetape4k/<repo>
git worktree add .worktrees/chore/bump-next-snapshot -b chore/bump-next-snapshot

# gradle.properties
# baseVersion=X.Y.Z  →  baseVersion=X.(Y+1).0
# snapshotVersion=   →  snapshotVersion=-SNAPSHOT

# CHANGELOG.md — add new unreleased section at top
# ## [X.(Y+1).0] — Unreleased
# ### Added
# ### Changed
# ### Fixed

git add gradle.properties CHANGELOG.md
git commit -m "chore: bump to X.(Y+1).0-SNAPSHOT and open CHANGELOG for next cycle"
git push -u origin chore/bump-next-snapshot

gh pr create \
  --base develop \
  --head chore/bump-next-snapshot \
  --title "chore: bump to X.(Y+1).0-SNAPSHOT"
```

---

### Step 13 — Local cleanup

```bash
git worktree remove .worktrees/release/X.Y.Z --force
git worktree remove .worktrees/chore/bump-next-snapshot --force
git branch -D release/X.Y.Z chore/bump-next-snapshot
git worktree prune --verbose
git fetch origin develop
git merge --ff-only origin/develop
```

---

## 4. Monitoring the Release Workflow

| Trigger | Workflow | Effect |
|---|---|---|
| PR merged to `develop` | `ci.yml` | Module test matrix |
| Nightly schedule | `nightly-tests.yml` | Full integration tests |
| Nightly success | `publish-snapshot.yml` | Publish `X.Y.Z-SNAPSHOT` to Maven Central Snapshots |
| Tag push `X.Y.Z` | `release.yml` | Publish release to Maven Central Portal + create GitHub Release |

---

## 5. Post-release Tasks

```bash
# Confirm GitHub Release
gh release view X.Y.Z

# Confirm Maven Central propagation (allow up to 30 minutes)
curl -s "https://repo1.maven.org/maven2/io/github/bluetape4k/<artifact>/X.Y.Z/<artifact>-X.Y.Z.pom" \
  -o /dev/null -w "%{http_code}"
```

- [ ] GitHub Release tag `X.Y.Z` created and visible
- [ ] Maven Central HTTP 200 for primary artifact
- [ ] Release notes updated (English + Korean bilingual)
- [ ] `bluetape4k-dependencies` version catalog bumped (PR merged) — Step 11
- [ ] Source repo bumped to next SNAPSHOT (PR merged) — Step 12
- [ ] Local worktrees and branches cleaned up — Step 13

---

## 6. Common Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `./gradlew build` succeeds but consumers fail to resolve | SNAPSHOT dependency not on Maven Central | Release the dependency repo first |
| Same version number assumed to be same release | GroupId-different repos have separate release cycles | Verify Maven Central HTTP 200 for each groupId independently |
| `release.yml` not triggered | `snapshotVersion` not empty, or tag format mismatch | Confirm tag equals `baseVersion`; `snapshotVersion` must be empty string |
| Nightly 1–2 failures ignored | Flake or real regression | Require 3 consecutive SUCCESS before releasing |
| Maven Central 404 after publish | Propagation delay (up to 30 min) | Recheck after 10 minutes |
| KDoc translation gaps | Agent translating by directory instead of file list | Scan with `rg -l "[가-힣]"` to build an explicit file list first |
| `release.yml` fails at "Verify gradle.properties" | `snapshotVersion` not empty, or `baseVersion` ≠ tag | Check both values match |
| `gh pr merge --delete-branch` local error | Branch checked out in main worktree | Cosmetic — GitHub merge succeeded; verify with `gh pr view --json state` |
| `git tag` fails "no tag message?" | Pre-push hook requires annotated tags | Use `git tag -a X.Y.Z -m "Release X.Y.Z"` |
| `git worktree add` fails "already exists" | Leftover from previous attempt | `rm -rf .worktrees/<path>` + `git worktree prune` + `git branch -D <branch>` |
| Local `develop` behind `origin/develop` | Reset ran before PR merged on GitHub | `git fetch origin develop && git merge --ff-only origin/develop` |
