# Workspace Guidance PR Triage

## Context

The local `.github` worktree still had an open WIP branch from a 2026-05-18
audit snapshot plus newer uncommitted workspace guidance edits.

## Decision or Finding

Do not merge stale `WIP.md` snapshots after a release train has materially
changed the ecosystem state. Salvage durable workspace guidance changes into a
fresh PR based on current `main`, and close the stale WIP PR.

## Outcome

The workspace guidance sync was separated from the old WIP snapshot so the
canonical `docs/workspace/AGENTS.md` and `docs/workspace/CLAUDE.md` can be
reviewed without carrying obsolete queue state.

## Verification

- Compared the open WIP PR against `origin/main`.
- Confirmed the untracked `.omc/state/last-tool-error.json` was a local tool
  error cache and not repository content.

## Future Guidance

Treat `WIP.md` as a short-lived snapshot. If it is more than a few days old or
the release state has moved on, close the WIP PR and create a narrower guidance
or process-documentation PR for reusable changes.
