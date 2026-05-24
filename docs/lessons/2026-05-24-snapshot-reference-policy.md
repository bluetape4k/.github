# Snapshot Reference Policy

## Context

Release runbooks needed to distinguish checked-in development versions from
workflow-injected snapshot publication versions.

## Decision

`baseVersion` is advanced to the next release version after every release, while
`snapshotVersion=` stays empty in `gradle.properties`. Snapshot publishing
injects `-PsnapshotVersion=-SNAPSHOT`; release publishing uses `baseVersion`
only. Internal `bluetape4k-*` references stay on matching `-SNAPSHOT` versions
during development and remove the suffix only in release-prep branches after the
upstream release is visible from Maven Central.

## Outcome

The central release runbook, governance note, and pre-release checklist now
describe the same snapshot/reference policy.

## Verification

- `git diff --check`

## Future Guard

Do not check `-SNAPSHOT` into `snapshotVersion`. If a development branch needs a
snapshot artifact, change the internal dependency reference, not the repository's
own checked-in snapshot suffix.
