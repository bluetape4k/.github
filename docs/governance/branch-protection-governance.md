# bluetape4k Branch Protection Governance

## Purpose

Governed repositories should route changes through pull requests. Direct pushes
to the default branch or release branch make release-train state hard to audit
and can bypass CI.

## Current Baseline

GitHub organization-level rulesets are preferred, but the bluetape4k
organization currently cannot use them without upgrading to GitHub Team. Until
that changes, repository-level rulesets are the active baseline.

The repository ruleset is named `bluetape4k default branch guard` and applies to:

- `~DEFAULT_BRANCH`
- `refs/heads/main`

Rules:

- Block branch deletion.
- Block non-fast-forward updates.
- Require changes through pull requests.
- Do not require approvals yet.
- Do not require status-check names yet.

Approvals and required status checks should be added after repository inventory
and workflow drift audits provide stable job names. Adding check names before
that would create brittle rules that break valid maintenance PRs.

## Documentation-Only PR Policy

Documentation-only PRs should not wait for heavyweight CI unless branch
protection explicitly requires a status check. The expected local gate is:

- review the changed documentation content;
- run `git diff --check`;
- run a repository-specific documentation build only when rendered docs,
  generated docs, or the public website are affected.

GitHub `Automatic Dependency Submission` / `submit-gradle` checks are useful
background signals, but they are non-blocking for documentation-only PRs unless
they are explicitly configured as required branch-protection checks.

## Operating Command

Audit:

```bash
python3 scripts/repo_ruleset_guard.py
```

Apply or refresh the baseline:

```bash
python3 scripts/repo_ruleset_guard.py --apply
```

## Scope

The governed scope includes the main bluetape4k libraries, `.github`, and the
selected workshop/example repositories. `ocean-workshop` and `kotlin-dev-agent`
remain excluded.
