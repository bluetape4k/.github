# bluetape4k Security Baseline

## Purpose

Security governance should make repository risk visible without turning every
pull request into a full security scan. The baseline separates always-on checks
from scheduled or release-sensitive checks.

## Baseline

Governed repositories should have:

- security reporting coverage through repository-local `SECURITY.md` or the
  organization default in `.github/SECURITY.md`,
- Dependabot enabled for Gradle and GitHub Actions,
- secret scanning through gitleaks in CI or an equivalent scheduled workflow,
- CodeQL for source-heavy repositories unless explicitly excluded,
- dependency graph visibility through dependency submission where useful.

## Trigger Policy

| Check | Recommended trigger |
|---|---|
| Gitleaks for changed content | Pull request CI. |
| Full-history secret scan | Scheduled security workflow or manual run. |
| CodeQL | Pull request when affordable, otherwise scheduled. |
| Dependency submission | CI on default branch and PRs where Gradle metadata changes. |
| Dependabot security updates | Automatic PRs, then validation by dependency risk tier. |

## Audit Command

```bash
python3 scripts/security_baseline_audit.py
```

The audit reports coverage only. Workflow normalization is intentionally left to
the repository inventory and workflow drift work so required checks are added
with stable job names instead of brittle guesses.
