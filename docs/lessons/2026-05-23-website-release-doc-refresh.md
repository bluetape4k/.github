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

For the 2026-05-23 release train, `bluetape4k.github.io` PR #11 updated the
public coordinates after `bluetape4k-dependencies 1.1.3` returned HTTP 200 from
Maven Central. GitHub Pages deployment run `26337058162` completed successfully,
and the live version governance page showed:

- `bluetape4k-dependencies` `1.1.3`
- `bluetape4k-bom` `1.9.1`
- `bluetape4k-exposed-bom` `1.9.1`
- `bluetape4k-aws-bom` `0.2.1`
- `bluetape4k-graph-bom` `0.4.1`
- `bluetape4k-leader-bom` `0.2.1`
- `bluetape4k-image-bom` `0.1.2`
- `bluetape4k-javers-bom` `0.1.2`
- `bluetape4k-text-bom` `0.1.2`

## Verification

- Updated `docs/release/central-portal-release-runbook.md`.
- Updated `docs/release/pre-release-checklist.md`.
- Ran Markdown and diff checks in this repository.
- Ran `npm run build` and `git diff --check` in `bluetape4k.github.io`.
- Verified the live `https://bluetape4k.github.io/ecosystem/version-governance/`
  page after Pages deployment.

## Future Guidance

For every release train, update `bluetape4k.github.io` immediately after
`bluetape4k-dependencies` is published and Maven Central returns HTTP 200 for
the imported BOMs. Verify `npm run build`, the Pages deployment run, and the
live version governance page before reporting the release complete.
