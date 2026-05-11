# Nightly Governance Needs Repo-Local Scope Contracts

## Context

Issue #2 split heavy bluetape4k Nightly jobs into daily smoke and weekly full
lanes. The organization `.github` repository dispatches Nightly workflows across
repositories, while each target repository owns its actual Gradle jobs and
coverage/runtime cost.

## Decision

Keep `smoke` and `full` as the common organization-level scope contract. Let
repositories expose specialized scopes only inside their own workflows, and map
only supported common inputs from `org-workflows.json`.

## Outcome

- Daily Nightly runs can stay fast by defaulting to smoke coverage.
- Weekly full Nightly keeps the broad integration signal.
- The central dispatcher avoids sending repo-specific scopes to workflows that
  do not support them.
- Heavy repositories document whether they are split, intentionally simple, or
  excluded from release dispatch.

## Verification

- `actionlint .github/workflows/org-nightly.yml`
- `python3 scripts/dispatch_org_workflows.py --kind nightly --repositories all --scope smoke --dry-run`
- `python3 scripts/dispatch_org_workflows.py --kind nightly --repositories all --scope full --dry-run`
- Repo-local `actionlint .github/workflows/nightly.yml` for split workflows.

## Future Guidance

- Merge target repository workflow changes before merging central dispatcher
  input changes.
- Treat central workflow inputs as stable public contracts; add only scopes that
  every mapped target can accept.
- Keep repository-specific heavy scopes in repo-local workflows unless the
  organization dispatcher has a clear cross-repository use case.
- When a workflow-only PR exposes unrelated compile failures, fix the failing
  repository before declaring the governance change complete.
