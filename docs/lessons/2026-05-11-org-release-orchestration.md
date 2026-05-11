# Org Release Orchestration Needs Dry-Run Gates

## Context

The bluetape4k organization is preparing for an official release at the end of
May 2026. Version drift, full Nightly dispatch, snapshot publishing, and release
dispatch need an organization-level operating surface.

## Decision

Keep the central orchestration in the organization `.github` repository, but do
not let it publish by default. Cross-repository snapshot and release workflows
must default to `dryRun=true` and require an explicit confirmation phrase before
dispatching real publishing workflows.

## Outcome

The central `.github` repository now owns:

- Shared version drift reporting.
- Organization Nightly dispatch planning.
- Snapshot dispatch planning and execution.
- Release train dispatch planning and execution.

Target repositories remain responsible for their own publishing credentials,
signing keys, package permissions, and release workflow behavior.

## Verification

- `python3 -m py_compile scripts/version_drift_report.py scripts/dispatch_org_workflows.py`
- `python3 scripts/version_drift_report.py --workspace ..`
- `python3 scripts/dispatch_org_workflows.py --kind nightly --scope full --dry-run`
- `python3 scripts/dispatch_org_workflows.py --kind snapshot --dry-run`
- `python3 scripts/dispatch_org_workflows.py --kind release --version 0.0.0 --dry-run`
- `actionlint .github/workflows/*.yml`

## Future Guidance

- Use `ORG_WORKFLOW_TOKEN` from a GitHub App installation token or fine-grained
  PAT with cross-repository Actions write access.
- Keep organization workflows as dispatchers only; avoid duplicating publish
  logic in the central repo.
- Add repo-local release workflows before including a repository in the release
  train; the central train should dispatch existing workflows, not invent target
  repository release behavior.
- Run snapshot train successfully before real release train dispatch.
- Treat drift report failures as release-freeze blockers unless the exception is
  documented in the release notes or a linked issue.
