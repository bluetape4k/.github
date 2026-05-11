# Workspace Guidance Needs a Canonical Repository Source

## Context

The bluetape4k workspace root contains guidance files such as `AGENTS.md`,
`CLAUDE.md`, and `WIP.md`, but the workspace root itself is not a Git
repository.

## Decision or Finding

Manage canonical copies in the organization `.github` repository and sync them
to the workspace root when needed.

## Outcome

The `.github` repository now stores workspace guidance under
`docs/workspace/` and provides `scripts/sync_workspace_docs.py` for drift checks
and synchronization.

## Verification

- `python3 -m py_compile scripts/sync_workspace_docs.py`
- `python3 scripts/sync_workspace_docs.py --check`

## Future Guidance

- Edit canonical workspace guidance in `.github/docs/workspace/`.
- Run `scripts/sync_workspace_docs.py --sync` when the active workspace-root
  copy should be refreshed.
- Commit `WIP.md` only for meaningful ecosystem snapshots.
