# Catalog and BOM Version Split

## Context

The 2026-05-23 release train exposed a cycle and an unnecessary artifact:
downstream `bluetape4k-*` repositories needed the shared Gradle catalog before
the final `bluetape4k-dependencies` BOM could exist. Publishing that catalog as
a separate Maven Central artifact was unnecessary because it is an internal
build input, not a user-facing dependency contract.

## Decision

Keep the distribution paths separate:

- `bluetape4k-dependencies` uses semantic versions for the final consumer BOM.
- `bluetape4k-dependencies/gradle/libs.versions.toml` is the internal
  build/contributor catalog source and is pinned by a git ref such as
  `catalog/2026-05-23-00`.
- downstream library repositories use `bluetape4kDependenciesCatalogPath` or
  `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH` to read the checked-out catalog file.

## Outcome

The release runbook and pre-release checklist now document the split. The
`bluetape4k-dependencies` build publishes only the BOM; internal catalog
consumption comes from a checked-out `bluetape4k-dependencies` ref.

## Verification

- Verified `projects`, `aws`, `text`, `graph`, `javers`, `exposed`, `leader`,
  and `image` settings can load a shared catalog from a local
  `bluetape4k-dependencies/gradle/libs.versions.toml` path.

## Future Rule

Do not use `bluetape4kDependenciesVersion` for Gradle catalog imports. Use it
only for actual `io.github.bluetape4k:bluetape4k-dependencies` platform
imports. Do not publish the internal build catalog as a Maven Central artifact
unless there is a separate user-facing reason.
