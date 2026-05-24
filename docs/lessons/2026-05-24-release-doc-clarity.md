# Release Documentation Clarity

## Context

The May 2026 release train required several follow-up edits because release
prep, snapshot publication, post-release reopen, and internal bluetape4k version
references were easy to mix up.

## Decision

Keep `Version Management Policy` as the canonical policy, then make the release
runbook explain execution phases with required evidence. The checklist should
state which branch phase it applies to instead of treating all SNAPSHOT
references as equally wrong.

## Outcome

The release runbook now starts with a flow map, the governance policy includes
version/reference state tables, and the pre-release checklist distinguishes
development snapshot references from release-prep non-snapshot references.

## Verification

- `git diff --check`

## Future Guard

When a release mistake happens, classify it by phase first: normal development,
snapshot validation, release prep, tag/release, post-release reopen, or final
dependencies BOM. Then update the phase gate instead of adding another isolated
warning.
