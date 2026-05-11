# Kover Governance Needs Baselines Before Gates

## Context

Issue #1 reviewed Kover coverage across bluetape4k repositories. Most
repositories already generate Kover reports, but only selected modules enforce
verification bounds.

## Decision or Finding

Do not enable broad failing coverage gates without measured baselines. Use
repo-local policy files to document whether a module is enforced, report-only,
or intentionally excluded.

## Outcome

The organization policy now separates core library targets, integration-heavy
targets, report-only transitions, and workshop/demo exceptions.

## Verification

- Central repository inventory created in
  `docs/governance/kover-coverage-governance.md`.
- Repo-local coverage policy files were added for each issue-scope repository.
- Existing `leader` Kover bounds are now run from Nightly.

## Future Guidance

- Prefer module-level `koverVerify` gates over one blunt repository threshold.
- Measure current line coverage before setting a failing bound.
- Keep integration-heavy exceptions explicit and time-boxed with a follow-up
  threshold plan.
