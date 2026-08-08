# 신규 모듈에는 Nightly 후속 작업이 필요하다

## 맥락

- `bluetape4k-graph` PR #100에서 `graph-ktor`와 `ktor-graph-examples`를
  추가했습니다.
- PR은 모듈 test를 직접 검증했지만 repository-local Nightly workflow에 새
  모듈 test job을 추가하지 않았습니다.
- 후속 PR에서 `graph-ktor` CI/Nightly job을 추가하며 workspace guidance도
  보강했습니다.

## 결정 또는 발견

- 신규 모듈은 code/build registration만으로 완료되지 않습니다.
  - 증거: `settings.gradle.kts`, README, BOM은 갱신했지만 Nightly workflow가
    빠져 `graph-ktor`가 예약된 full validation에서 누락될 수 있었습니다.
  - 다음 guard: 신규 모듈 DoD에 CI와 Nightly workflow grep을 포함합니다.
- Nightly는 CI보다 넓은 validation boundary를 보장하는 gated workflow입니다.
  - 증거: `graph-ktor:test`는 backend Testcontainers smoke를 포함하므로 daily
    smoke보다 Full Nightly에 넣어야 합니다.
  - 다음 guard: 모듈 test 비용을 smoke/full로 분류하고 container-backed
    모듈은 보통 Full Nightly job으로 추가합니다.

## 결과

- `docs/workspace/AGENTS.md`에 신규 모듈 생성 시 CI/Nightly workflow 갱신
  지침을 추가했습니다.
- `docs/workspace/AGENTS.md`에 Nightly workflow 변경 시 `workflow_dispatch`
  실행과 run URL/result 기록을 요구했습니다.
- `docs/governance/nightly-workflow-governance.md`에 신규 모듈 Nightly
  follow-up 기준을 추가했습니다.

## 검증

`graph-ktor` job을 포함한 CI/Nightly workflow diff와 실제 dispatch 결과를
대조했습니다.
