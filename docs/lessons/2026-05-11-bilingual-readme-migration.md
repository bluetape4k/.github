# Bilingual README Migration Needs Paired Ownership

## Context

Recent documentation work moved bluetape4k example and application README files
toward paired English and Korean documentation.

## Decision or Finding

Treat `README.md` and `README.ko.md` as one documentation surface. Any public
behavior, setup, or usage change that touches one language should check the
other language in the same PR.

## Outcome

Workspace guidance now requires bluetape4k module README pairs and a language
switch directly below the title.

## Verification

- Workspace `AGENTS.md` documents the paired README rule.
- Recent README migration PRs used the English/Korean pair shape.

## Future Guidance

- Do not leave Korean-only or English-only module README updates unless the
  repository explicitly documents an exception.
- For large README migrations, update module README files in batches and keep
  link labels identical across languages.
