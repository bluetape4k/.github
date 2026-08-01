# AGENTS.md - bluetape4k .github

This repository inherits the workspace guidance from `../AGENTS.md`.
Read and follow the workspace root guide first. This file only adds
organization-profile, workflow-template, and workspace-guide rules.

This repository owns shared GitHub community files, organization profile
content, reusable guidance documents, and workspace-level agent instructions.

## Mandatory Workflow Gate

For every task under `/Users/debop/work/bluetape4k`, the first action is to
invoke and complete `$bluetape-workflow`. It is mandatory for classification,
planning approval, execution gates, verification, and DoD reporting; no work
may bypass it.

For implementation or code review, load and follow the matching language
pattern skill before touching code: `$bluetape-kotlin-patterns`,
`$bluetape-go-patterns`, `$bluetape-py-patterns`, or `$bluetape-rs-patterns`.
Repo-local guidance may add narrower rules, but it must not weaken this gate.

## Layout

- `docs/workspace/AGENTS.md` is the source file for the workspace root
  `AGENTS.md` symlink used under `/Users/debop/work/bluetape4k`.
- `profile/` contains the organization profile README and shared visual assets.
- `scripts/` contains helper scripts for organization maintenance.
- `org-workflows.json` tracks organization workflow metadata.

## Rules

- Keep `docs/workspace/AGENTS.md` concise and common. Repo-local rules belong in
  the target repository's own `AGENTS.md`.
- Do not add repo-specific module lists or build commands to the workspace root
  guide unless the rule applies across the ecosystem.
- When changing GitHub templates or shared guidance, verify downstream wording
  for issue/PR metadata, language policy, and README locale policy.

## Verification

- For documentation-only guidance changes, run `git diff --check`.
- For scripts, run the targeted script check or dry-run mode when available.
