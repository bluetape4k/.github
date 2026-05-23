# Documentation-Only PR CI Policy

## Context

Small documentation cleanup PRs were waiting on repository build and dependency
submission checks even when the only changes were Markdown path corrections.
This added release-train overhead without improving confidence.

## Decision

Treat documentation-only PRs as local-documentation-gated work:

- content review plus `git diff --check` is sufficient for plain Markdown,
  lessons, specs, plans, and governance text;
- run a documentation build only when rendered docs, generated docs, or the
  public website are affected;
- do not wait for heavyweight CI or GitHub `Automatic Dependency Submission`
  unless branch protection marks the check required.

## Outcome

Workspace guidance and branch-protection governance now encode the policy so
future cleanup PRs can merge without unnecessary CI waiting.

## Verification

- `git diff --check`
- `python3 scripts/sync_workspace_docs.py --check`

## Future Guidance

Do not disable security or dependency-submission automation solely for docs
cleanup. Let background checks run if GitHub starts them, but do not treat them
as release or merge gates for documentation-only PRs unless the repository
ruleset requires them.
