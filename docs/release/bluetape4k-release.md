# bluetape4k Release Process

Standard release procedure for any `bluetape4k-*` repository.
Validated against `bluetape4k-projects` 1.8.0 release (2026-05-17).

---

## Prerequisites

- `develop` branch is green (Nightly CI all SUCCESS)
- All hard-blocker issues closed
- CHANGELOG `## [X.Y.Z] — Unreleased` section up to date
- `gradle.properties`: `baseVersion=X.Y.Z`, `snapshotVersion=-SNAPSHOT`

---

## Step 1 — Pre-release cleanup

Remove stale/unused version properties before cutting a release branch.

```bash
# Check for unused version properties (e.g., exposedVersion)
rg "Version=" gradle.properties
rg "val \w+Version: String by project" build.gradle.kts

# Verify nothing references the property in submodules
rg "<property>" --include="*.kts" | grep -v "build.gradle.kts"
```

Remove any properties that have zero submodule references.

---

## Step 2 — Create release branch (in worktree)

```bash
git worktree add .worktrees/release/X.Y.Z -b release/X.Y.Z
```

---

## Step 3 — Edit release prep files

**`gradle.properties`**

```diff
-snapshotVersion=-SNAPSHOT
+snapshotVersion=
```

Also remove any unused `*Version` properties discovered in Step 1.

**`build.gradle.kts`**

Remove corresponding `val <property>: String by project` declarations for removed properties.

**`CHANGELOG.md`**

```diff
-## [X.Y.Z] — Unreleased
+## [X.Y.Z] — YYYY-MM-DD
```

---

## Step 4 — Commit, push, create PR

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

## Step 5 — Wait for CI and merge

```bash
# Poll until all checks complete
gh pr view <PR#> --json statusCheckRollup \
  --jq '[.statusCheckRollup[]] | {total:length, done:[.[]|select(.status=="COMPLETED")]|length, failed:[.[]|select(.conclusion=="failure")]|length}'

# Merge when all done=total and failed=0
gh pr merge <PR#> --squash --delete-branch
```

> **Note:** if `develop` is checked out in the main worktree, `--delete-branch` may fail locally but the GitHub-side merge still succeeds. Verify with `gh pr view <PR#> --json state`.

---

## Step 6 — Sync local develop

```bash
git fetch origin develop
git merge --ff-only origin/develop
git log --oneline -3
```

Confirm the release prep commit is at HEAD and `snapshotVersion=` is empty.

```bash
grep "baseVersion\|snapshotVersion" gradle.properties
# Expected:
# baseVersion=X.Y.Z
# snapshotVersion=
```

---

## Step 7 — Tag and push → triggers Publish Release workflow

The `release.yml` workflow fires on any tag matching `[0-9]+.[0-9]+.[0-9]+`.

```bash
git tag -a X.Y.Z -m "Release X.Y.Z"
git push origin X.Y.Z
```

Verify the workflow started:

```bash
sleep 5
gh run list --workflow="release.yml" --limit 3
```

---

## Step 8 — Monitor Publish Release workflow

```bash
gh run view <RUN_ID> --json status,conclusion,jobs \
  --jq '{status:.status, conclusion:.conclusion, jobs:[.jobs[]|{name:.name,status:.status,conclusion:.conclusion}]}'
```

Expected jobs (in order):

1. `Resolve release version` — validates tag format and `gradle.properties` match
2. `Publish RELEASE to Maven Central Portal` — runs `publishAggregationToCentralPortal`
3. `Create GitHub Release` — reads `CHANGELOG.md` section, generates release notes

All three must reach `conclusion: success`.

---

## Step 9 — Verify GitHub Release

```bash
gh release view X.Y.Z --json tagName,publishedAt,url
```

---

## Step 10 — Update release notes (bilingual)

Edit the auto-generated release notes to add English + Korean `<details>` blocks:

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

## Step 11 — Update `bluetape4k-dependencies`

Update the version ref in the ecosystem catalog:

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
  --json statusCheckRollup --jq '...'   # same pattern as Step 5

gh pr merge <PR#> --repo bluetape4k/bluetape4k-dependencies --squash --delete-branch
```

---

## Step 12 — Bump to next SNAPSHOT in source repo

```bash
cd ~/work/bluetape4k/<repo>
git worktree add .worktrees/chore/bump-next-snapshot -b chore/bump-next-snapshot

# gradle.properties
# baseVersion=X.Y.Z  →  baseVersion=X.(Y+1).0
# snapshotVersion=   →  snapshotVersion=-SNAPSHOT

# CHANGELOG.md — add new unreleased section at top (after the existing [Unreleased] header)
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

Wait for CI and merge (same as Step 5).

---

## Step 13 — Local cleanup

```bash
# Remove release worktrees
git worktree remove .worktrees/release/X.Y.Z --force
git worktree remove .worktrees/chore/bump-next-snapshot --force

# Delete local merged branches
git branch -D release/X.Y.Z chore/bump-next-snapshot

# Prune stale worktree registrations
git worktree prune --verbose

# Sync develop to latest
git fetch origin develop
git merge --ff-only origin/develop
```

---

## Workflow trigger summary

| Trigger | Workflow | Effect |
|---------|----------|--------|
| PR merged to `develop` | `ci.yml` | Module test matrix |
| Nightly schedule | `nightly-tests.yml` | Full integration tests |
| Nightly success | `publish-snapshot.yml` | Publish `X.Y.Z-SNAPSHOT` to Maven Central Snapshots |
| Tag push `X.Y.Z` | `release.yml` | Publish release to Maven Central Portal + create GitHub Release |

---

## Checklist

```
Pre-release
[ ] Nightly CI: all SUCCESS
[ ] All hard-blocker issues closed
[ ] CHANGELOG [X.Y.Z] — Unreleased section complete

Release branch (Steps 2–6)
[ ] snapshotVersion= (empty)
[ ] Unused *Version properties removed from gradle.properties + build.gradle.kts
[ ] CHANGELOG date stamped (YYYY-MM-DD)
[ ] PR CI: all checks SUCCESS before merge
[ ] Local develop fast-forwarded to HEAD

Tag + publish (Steps 7–9)
[ ] Tag X.Y.Z pushed
[ ] release.yml: 3/3 jobs SUCCESS
[ ] GitHub Release created and visible

Post-release (Steps 10–13)
[ ] Release notes updated (English + Korean bilingual)
[ ] bluetape4k-dependencies bumped to X.Y.Z (PR merged)
[ ] Source repo bumped to X.(Y+1).0-SNAPSHOT (PR merged)
[ ] Local worktrees and branches cleaned up
```

---

## Common pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `release.yml` fails at "Verify gradle.properties" | `snapshotVersion` not empty, or `baseVersion` mismatch | Check tag name == `baseVersion`; `snapshotVersion` must be empty string |
| `gh pr merge --delete-branch` local error | Branch checked out in main worktree | Cosmetic — merge already succeeded on GitHub side. Verify with `gh pr view --json state` |
| `git tag` fails with "no tag message?" | Pre-push hook requires annotated tags | Use `git tag -a X.Y.Z -m "Release X.Y.Z"` |
| `git worktree add` fails "already exists" | Leftover directory from previous attempt | `rm -rf .worktrees/<path>` + `git worktree prune` + `git branch -D <branch>` |
| Local `develop` behind `origin/develop` | `reset --hard` ran before PR was merged on GitHub | `git fetch origin develop && git merge --ff-only origin/develop` |
| `git branch -D` fails in chain after `worktree remove` | Shell cwd was inside the removed worktree | Use absolute paths or run each command separately |
