# Workspace Documents

This directory is the canonical source for bluetape4k workspace-root guidance
files that live outside any single repository checkout.

Tracked source files:

- `AGENTS.md` - Codex workspace contract.
- `CLAUDE.md` - Claude workspace contract.
- `WIP.md` - ecosystem-level work queue snapshot.

The active runtime copies live at the workspace root:

- `../AGENTS.md`
- `../CLAUDE.md`
- `../WIP.md`

Use `scripts/sync_workspace_docs.py --check` to detect drift and
`scripts/sync_workspace_docs.py --sync` from the `.github` repository to refresh
the workspace-root copies from this canonical directory.

`WIP.md` changes often. Commit only meaningful snapshots, not every local queue
scratch update.
