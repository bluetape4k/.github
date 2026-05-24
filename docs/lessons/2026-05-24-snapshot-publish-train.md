# Snapshot Publish Train

## Context

After the May 2026 release train, each `bluetape4k-*` repository was reopened
to the next development line with `snapshotVersion=` empty and internal
`bluetape4k-*` references restored to matching `-SNAPSHOT` versions. The train
then had to be validated by real `publish-snapshot.yml` runs in dependency
order.

## Decision or Finding

Treat post-release snapshot publishing as its own dependency-ordered train, not
as an informal follow-up to release prep. The train must publish and verify
`projects` first, then downstream repos, then `bluetape4k-dependencies` last.

Do not assume workflow inputs are uniform across repositories. Some
`publish-snapshot.yml` files do not accept `diagnoseSigning`.

Snapshot artifact availability must be verified through Central snapshot
`maven-metadata.xml`; release Maven Central POM URLs are the wrong evidence for
`-SNAPSHOT` versions.

## Outcome

The release runbook now has a `Post-release Snapshot Publish Train` section with
the dependency order, dispatch command, metadata verification URL shape, and
`bluetape4k-dependencies` snapshot verifier command.

The pre-release checklist and version governance policy now call out snapshot
metadata evidence and repo-specific snapshot workflow inputs.

## Verification

- `git diff --check`
- Markdown heading inventory reviewed with `rg -n '^#' docs/release docs/governance docs/lessons`

## Future Guidance

After every release, open the next development line first, then run the snapshot
publish train in order. Record PR URLs, publish run IDs, and snapshot metadata
timestamps before starting release prep for any downstream consumer of those
snapshots.
