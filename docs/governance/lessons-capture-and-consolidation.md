# Lessons Capture and Consolidation

## Purpose

Lessons are durable operational memory for the bluetape4k organization. They
capture what changed, what failed, what evidence resolved it, and what future
work should do differently.

Runtime notes, chat summaries, and `.omx` state are transient. Promote only
stable, reusable findings into repository documentation.

## Repository Contract

Every active bluetape4k repository should keep a tracked `docs/lessons/`
directory. If a repository does not maintain lessons, document the reason in
the central inventory and revisit it when the repository becomes active.

Each repository should include:

- `docs/lessons/README.md` with repo-local lesson rules.
- One lesson file per significant event, named `YYYY-MM-DD-{slug}.md`.
- Links from central issues or PRs when a lesson explains governance decisions.

## Workspace Guidance Contract

Workspace-root guidance files live outside a normal Git repository, so the
organization `.github` repository owns canonical copies under `docs/workspace/`.

Tracked workspace files:

- `AGENTS.md`
- `CLAUDE.md`
- `WIP.md`

Use `scripts/sync_workspace_docs.py --check` to detect drift and
`scripts/sync_workspace_docs.py --sync` to refresh the active workspace-root
copies.

## Lesson Template

Use `docs/templates/lesson.md` as the reusable template.

Required sections:

- Context
- Decision or Finding
- Outcome
- Verification
- Future Guidance

Keep lessons concise. Store evidence such as commands, PR links, issue links,
or workflow runs, but do not paste long logs.

## Daily or Session Consolidation

At the end of substantial work:

1. Scan new repo-local lessons and recent PRs.
2. Merge duplicate lessons or link related entries.
3. Promote repeatable rules into `AGENTS.md`, workflow docs, or skills.
4. Keep event-specific evidence in the lesson file.
5. Update central issue comments when the lesson closes a governance item.

## Current Inventory

| Repository | Lessons status | Notes |
|---|---|---|
| `bluetape4k-aws` | Active | Assertion migration lesson exists; README normalized. |
| `bluetape4k-dependencies` | Ready | README added for future release/BOM lessons. |
| `bluetape4k-experimental` | Ready | README added; keep experimental runtime findings here. |
| `bluetape4k-exposed` | Active | Document storage lesson exists; README normalized. |
| `bluetape4k-graph` | Ready | README added for graph/runtime lessons. |
| `bluetape4k-image` | Ready | README added for image processing and native dependency lessons. |
| `bluetape4k-javers` | Ready | README added for audit/diff integration lessons. |
| `bluetape4k-leader` | Active | Rich lesson history exists; README normalized. |
| `bluetape4k-projects` | Active | Existing virtual-thread lesson plus Kover aggregation backfill. |
| `bluetape4k-text` | Ready | README added for tokenizer/language detection lessons. |
| `bluetape4k-workshop` | Active | Nightly dependency lesson backfilled. |

## Promotion Rules

- A one-time failure stays in `docs/lessons/`.
- A repeated failure becomes checklist guidance.
- A rule that changes implementation behavior belongs in repo-local
  `AGENTS.md` or a narrow skill.
- Organization-wide workflow behavior belongs in `.github/docs/governance/`.
