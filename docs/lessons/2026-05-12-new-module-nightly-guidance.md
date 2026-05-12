# 신규 모듈 Nightly 지침 Lessons

## Context

- `bluetape4k-graph` PR #100에서 `graph-ktor`와 `ktor-graph-examples`가 추가됐다.
- PR은 module test를 직접 검증했지만, repository-local Nightly workflow에 신규 module test job을 추가하지 않았다.
- 후속 PR에서 `graph-ktor` CI/Nightly job을 추가하면서 workspace guidance도 보강했다.

## Decision or Finding

- Lesson: 신규 module 생성은 code/build registration만으로 끝나지 않는다.
  - Evidence: `settings.gradle.kts`, README, BOM은 갱신됐지만 Nightly workflow가 빠져 `graph-ktor`가 scheduled full validation에서 누락될 수 있었다.
  - Future guard: 신규 module 작업의 DoD에는 CI와 Nightly workflow grep을 포함한다.

- Lesson: Nightly는 CI보다 넓은 validation boundary를 보장하는 gated workflow다.
  - Evidence: `graph-ktor:test`는 backend Testcontainers smoke를 포함하므로 daily smoke보다 Full Nightly에 넣는 것이 맞다.
  - Future guard: module test cost를 smoke/full로 분류하고, container-backed module은 보통 Full Nightly job으로 추가한다.

## Outcome

- `docs/workspace/AGENTS.md`에 신규 module 생성 시 CI/Nightly workflow 갱신 지침을 추가했다.
- `docs/governance/nightly-workflow-governance.md`에 신규 module Nightly follow-up criterion을 추가했다.

## Verification

- Docs-only change.
- `git diff --check`

## Future Guidance

- 신규 module PR checklist:
  - `settings.gradle.kts` registration 확인.
  - `README.md` / `README.ko.md` 갱신.
  - `bom` 또는 dependency docs 영향 확인.
  - `.github/workflows/ci.yml` module path filter와 test job 확인.
  - `.github/workflows/nightly.yml` smoke/full scope에 module test 추가.
  - Lessons 작성.
