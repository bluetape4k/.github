# Lessons Learned: Organization Governance Automation

## Context

The bluetape4k organization added governance automation for dependency updates,
branch protection, security baseline visibility, and repository inventory drift.

## Lessons

- Dependabot should generate update PRs, but it should not assign every PR to a
  human by default. Default assignees create notification floods as soon as
  Dependabot is enabled across many repositories.
- Cross-repository consistency cannot be delegated to Dependabot alone.
  Dependabot is repository-scoped; `.github` needs central version drift and
  governance drift audits.
- Compatibility-line aliases must be protected from automated semver-major
  upgrades. Aliases such as `kafka3`/`kafka4`, `jackson2`/`jackson3`, and
  `spring-boot3`/`spring-boot4` encode supported platform lines, but Dependabot
  only sees Maven coordinates or plugin IDs and can incorrectly rewrite the
  older line to the newer major.
- Not every dependency update deserves Full Nightly. A tiered validation ladder
  is cheaper and more useful: repository CI for local updates, affected Nightly
  for shared runtime/compiler/container/serialization dependencies, and Full
  Nightly near release freeze or major upgrades.
- GitHub organization rulesets are preferable, but they require GitHub Team for
  this organization. Repository-level rulesets are the practical baseline until
  the plan changes.
- Required status checks should wait until workflow job names are inventoried
  and stable. Prematurely pinning check names creates brittle branch protection.
- A central `.github/SECURITY.md` gives default security policy coverage, but
  repositories still need workflow-level scanning visibility.
- Governance scripts should have dry-run/audit modes and produce Markdown
  summaries so scheduled workflows and humans read the same evidence.

## Follow-up

- Use the new repository inventory before adding required status checks.
- Triage Dependabot PRs by risk group instead of merging everything
  mechanically.
- Normalize dependency submission and CodeQL coverage after repository
  categories are finalized.
