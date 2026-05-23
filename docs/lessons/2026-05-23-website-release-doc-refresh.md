# Website Release Documentation Refresh

## Context

The 2026-05-23 release train published updated `bluetape4k-dependencies` and
library BOM versions, then required a separate `bluetape4k.github.io` update so
public setup examples and version governance pages matched Maven Central.

## Decision or Finding

The Central Portal release runbook must include a mandatory website
documentation refresh after the final BOM release is visible from Maven
Central. The release is not operationally complete until the public website
shows the current coordinates.

## Outcome

The shared release runbook now names the website pages to update, the local
website build checks to run, and the GitHub Pages/live-page evidence to record.
The pre-release checklist also treats the website update as a post-release
check.

## Verification

- Updated `docs/release/central-portal-release-runbook.md`.
- Updated `docs/release/pre-release-checklist.md`.
- Ran Markdown and diff checks in this repository.

## Future Guidance

For every release train, update `bluetape4k.github.io` immediately after
`bluetape4k-dependencies` is published and Maven Central returns HTTP 200 for
the imported BOMs. Verify `npm run build`, the Pages deployment run, and the
live version governance page before reporting the release complete.
