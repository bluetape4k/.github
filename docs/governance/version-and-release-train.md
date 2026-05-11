# bluetape4k Version Governance and Release Train

## Purpose

This document supports the planned official release at the end of May 2026.
It defines the central operating surface for shared dependency drift checks,
organization-wide Nightly dispatch, snapshot publishing, and release train
dispatch.

## Token Requirement

Cross-repository workflow dispatch requires an organization-scoped token. The
central `.github` repository must define `ORG_WORKFLOW_TOKEN` as a repository or
organization secret.

Recommended token shape:

- GitHub App installation token or fine-grained PAT.
- Repository access: all bluetape4k repositories managed by the train.
- Permissions:
  - Actions: read and write.
  - Contents: read.
  - Metadata: read.

The central workflows only dispatch existing repository workflows. Publishing
credentials, signing keys, and package permissions remain in each target
repository.

## Central Workflows

| Workflow | Purpose | Default safety |
|---|---|---|
| `Org Version Drift` | Clone bluetape4k repos and generate shared version drift report. | Weekly report; optional fail-on-drift. |
| `Org Nightly Dispatch` | Trigger Nightly workflows across selected repositories. | Manual only; `dryRun=true` by default. |
| `Org Snapshot Dispatch` | Trigger snapshot publishing workflows in train order. | Manual only; `dryRun=true`; confirmation phrase required for real dispatch. |
| `Org Release Train` | Trigger release workflows in train order. | Manual only; `dryRun=true`; confirmation phrase required for real dispatch. |

## Train Order

Snapshot dispatch uses this default order:

1. `bluetape4k-projects`
2. `bluetape4k-exposed`
3. `bluetape4k-aws`
4. `bluetape4k-graph`
5. `bluetape4k-image`
6. `bluetape4k-javers`
7. `bluetape4k-leader`
8. `bluetape4k-text`
9. `bluetape4k-dependencies`

`bluetape4k-dependencies` is last because it is the ecosystem BOM and should be
published after the libraries it coordinates.

Release dispatch currently uses the same order without `bluetape4k-dependencies`
because that repository has a snapshot workflow but no release workflow yet.
`bluetape4k-experimental` and `bluetape4k-workshop` are Nightly-only by default.

## Release Preconditions

Before running `Org Release Train` with `dryRun=false`:

- Shared version drift report has no unplanned drift.
- Each target repository has a matching release tag for the requested version.
- Repository-local release workflows have passed in `dryRun` or diagnostic mode.
- Snapshot train has succeeded for the same dependency state.
- GitHub Packages publishing and signing secrets are valid in target repos.

## Snapshot Preconditions

Before running `Org Snapshot Dispatch` with `dryRun=false`:

- Target repositories are on the intended `develop` state.
- Version drift is either aligned or documented.
- Nightly failures are understood or intentionally waived.
- The caller typed `deploy snapshots` in the confirmation input.

## Drift Policy

Organization-governed version groups are tracked by
`scripts/version_drift_report.py`:

- Kotlin
- Spring Boot
- Testcontainers
- Jackson 2 and Jackson 3
- Exposed
- AWS Kotlin SDK and Smithy Kotlin
- Kover
- Apache Fory

Allowed drift must be documented in the release notes or a linked issue before
release freeze. Experimental and Java 25-only modules may deviate when the
reason is explicit.
