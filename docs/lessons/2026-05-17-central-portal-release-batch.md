# 2026-05-17 Central Portal release batch

## Context

The workspace released the bluetape4k library set to Maven Central through
Central Portal. `bluetape4k-projects 1.8.0` had already been released, so the
batch covered the remaining publishable repositories and finished with
`bluetape4k-dependencies 1.0.0`.

Published artifacts:

- `bluetape4k-aws 0.1.0`
- `bluetape4k-text 0.1.0`
- `bluetape4k-graph 0.3.0`
- `bluetape4k-javers 0.1.0`
- `bluetape4k-exposed 1.8.0`
- `bluetape4k-leader 0.1.0`
- `bluetape4k-image 0.1.0`
- `bluetape4k-dependencies 1.0.0`

## Decisions

- Keep `gradle.properties` release-stable with `baseVersion=<release>` and
  `snapshotVersion=`. Snapshot publishing should pass
  `-PsnapshotVersion=-SNAPSHOT` instead of editing the file.
- Use repo-specific BOM version keys such as `bluetape4k-bom` and
  `bluetape4k-exposed-bom`; avoid ambiguous shared keys like `bluetape4k`.
- Exclude `experimental`, `workshop`, examples, demos, and benchmarks from
  release artifacts.
- Publish `bluetape4k-dependencies` last, only after every imported BOM is
  visible from Maven Central with HTTP 200.
- Use rebase merge for release-prep PRs and tag pushes for release workflows.

## Problems Found

### Missing dependency versions in generated POMs

`aws`, `exposed`, `leader`, and `image` needed Spring dependency-management POM
customization enabled for published modules. Disabling it with
`generatedPomCustomization { setEnabled(false) }` can leave dependencies without
versions in generated Maven POMs, which Central validation rejects.

### SNAPSHOT dependency drift

`graph` still referenced a `bluetape4k` SNAPSHOT version. Release preflight must
scan catalogs and generated POMs for `SNAPSHOT` before tagging.

### Non-library modules in release metadata

Examples, demos, and benchmarks must be excluded consistently from:

- BOM constraints
- NMCP aggregation
- publication/signing setup
- generated `bluetape4k-dependencies` catalog and constraints

Filtering only aggregation is insufficient if a module still has
`maven-publish`. Nested examples create both `:examples` and `:examples:*`, so
both forms must be excluded.

### Central Portal accepted vs Maven Central visible

GitHub Actions success means Central Portal accepted the publication. Public
consumer availability requires a separate HTTP 200 check against
`repo.maven.apache.org`. Propagation took several minutes for some artifacts.

### Shell variable footgun

In zsh, `path` is tied to `PATH`. A polling loop using `for path in ...` broke
`curl` and `sleep` inside the shell. Use `artifact_path`.

## Outcome

All targeted release workflows completed successfully and representative Maven
Central POM URLs returned HTTP 200. Follow-up PRs standardized BOM/NMCP filters
across published repositories and updated `bluetape4k-dependencies` generation.

## Verification Evidence

- `leader 0.1.0`: release workflow succeeded; `bluetape4k-leader-bom` and
  `bluetape4k-leader-core` POMs returned HTTP 200.
- `image 0.1.0`: release workflow succeeded; `bluetape4k-image-bom` and
  `bluetape4k-images` POMs returned HTTP 200.
- `dependencies 1.0.0`: release workflow succeeded; `bluetape4k-dependencies`
  and `bluetape4k-version-catalog` POMs returned HTTP 200.
- Imported BOM preflight before `dependencies` returned HTTP 200 for:
  `projects`, `aws`, `image`, `text`, `graph`, `leader`, `exposed`, and
  `javers`.

## Next Time

1. Start with `.github/docs/release/pre-release-checklist.md`.
2. Follow `.github/docs/release/central-portal-release-runbook.md` exactly.
3. Run generated POM checks before any tag push.
4. If Central validation fails, fix through a PR, merge to `develop`, then
   retag the failed version with `--force-with-lease`.
5. Do not release `bluetape4k-dependencies` until every imported BOM is publicly
   visible on Maven Central.
