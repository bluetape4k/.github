# Workshop Consumer BOM Policy

## Context

Release-upgrade work for May 2026 showed that workshop and application
repositories can drift when they pin individual bluetape4k artifacts while also
importing `bluetape4k-dependencies`.

## Decision

Workspace governance now treats workshop, example, and application repositories
as consumers. They should keep `bluetape4k-dependencies` as the only bluetape4k
version source and declare `io.github.bluetape4k*` artifacts without versions.

## Outcome

The policy was added to dependency governance, release-train governance, and
the release checklist so future release-upgrade PRs check the same rule.

## Verification

Documentation-only change. Verified with `git diff --check`.

## Future Guidance

When upgrading consumer repositories, grep for direct bluetape4k version refs
before opening PRs. Keep historical alias names only when needed for source
compatibility, and make those aliases versionless.
