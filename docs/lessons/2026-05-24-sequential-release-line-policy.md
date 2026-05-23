# Sequential Release Line Policy

## Context

`bluetape4k-projects` had both `1.9.2` and `1.10.0` milestones open after the
`1.9.1` release train. A stale PR attempted to move `develop` directly to
`1.10.0`, but `1.9.2` still owned the next patch line.

## Decision

Use sequential release-line work by default:

- keep `develop` on the currently active release line;
- finish or explicitly defer an active patch milestone before moving `develop`
  to the next minor line;
- create `release/X.Y.x` maintenance branches only on demand, from the last
  released tag, when a patch hotfix is needed after `develop` has advanced.

## Outcome

`bluetape4k-projects` opened the `1.9.2` development line first. The `1.10.0`
Ktor module family remains the next minor lane after the `1.9.2` patch line is
handled or explicitly deferred.

## Verification

- Updated `docs/governance/version-and-release-train.md`.
- Updated `docs/release/pre-release-checklist.md`.
- `git diff --check`

## Future Guidance

Patch fixes made on `release/X.Y.x` must be forward-ported to `develop`.
Feature/API work for the next minor line must stay on `develop` and must not be
backported into maintenance branches.
