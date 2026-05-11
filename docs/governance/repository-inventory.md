# bluetape4k Repository Inventory

## Purpose

`org-workflows.json` is the central machine-readable inventory for governed
repositories. It drives workflow dispatch and records governance expectations
for release, snapshot, Nightly, Dependabot, security, and coverage policy.

## Governed Flags

Each entry under `governance` defines:

- `default_ref`: expected integration branch.
- `dependabot`: whether `.github/dependabot.yml` is expected.
- `security`: whether security policy and security workflow coverage are
  expected.
- `coverage`: `policy` when `docs/governance/kover-coverage-policy.md` is
  expected, `report-only` when coverage is tracked without a local policy doc,
  otherwise `excluded`.
- `release`, `snapshot`, `nightly`: whether the repository participates in that
  train.

## Audit Command

```bash
python3 scripts/workflow_drift_audit.py --workspace ..
```

Use `--fail-on-drift` in CI once expected security and workflow categories are
fully normalized.

## Exclusions

`ocean-workshop` and `kotlin-dev-agent` are intentionally excluded from this
inventory. Add them only if their operational ownership changes.
