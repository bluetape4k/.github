# Spring Boot 4 Only README Policy

## Context

The organization profile README still described bluetape4k as supporting
Spring Boot 3/4. The current policy is that supported Spring integrations are
Spring Boot 4.x only.

## Decision or Finding

README support statements must describe Spring Boot 4.x as the only supported
Spring Boot line. Spring Boot 3 may still appear in historical migration notes,
comparison tables, removed-support notices, or legacy-helper warnings, but not
as a current support claim.

## Outcome

- Updated the organization profile README pair to remove Spring Boot 3/4
  compatibility language.
- Updated stale `bluetape4k-workshop` README headings/descriptions that still
  called Boot 4 examples "Spring Boot 3".
- Updated `bluetape4k-projects` OpenTelemetry README pair so the old WebFlux
  helper is framed as legacy/migration reference, not current Boot 3 support.

## Verification

- `rg --hidden -n -i "Spring Boot 3/4|Spring Boot 3\\.x/4\\.x|Spring Boot 3 and 4" /Users/debop/work/bluetape4k --glob 'README*.md' --glob '!**/.worktrees/**' --glob '!**/build/**'`
  returned no matches.
- Follow-up README searches found only removed-support statements, migration
  comparisons, legacy helper warnings, or external article references.

## Future Guidance

When README files mention Spring Boot support, use "Spring Boot 4.x only" for
current support. Do not restore generic Spring Boot 3/4 compatibility language.
