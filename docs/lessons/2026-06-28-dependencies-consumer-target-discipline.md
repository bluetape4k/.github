# Dependencies Consumer Target Discipline

## Context

2026-06-28 `bluetape4k-dependencies` release train closeout에서 workshop,
example, app consumer repositories를 `1.3.0`으로 마무리할 수 있었는데,
Maven Central에 `bluetape4k-dependencies 1.3.1`이 이미 보인다는 사실을
consumer sync target 변경 승인으로 잘못 취급했다.

그 결과 사용자가 요구한 "example repos는 dependencies 1.3.0으로 올리면
된다"는 범위를 벗어나 consumer repositories를 `1.3.1`로 올렸다. 이는
기술적 필요가 아니라 release target control 실패였다.

## Decision or Finding

Consumer sync target은 다음 순서로만 정한다.

1. 최신 사용자 지시.
2. release checklist에 명시된 train target.
3. 사용자가 명시적으로 승인한 corrective patch target.

Maven Central에 더 최신 patch가 보인다는 사실만으로 consumer target을
바꾸면 안 된다. immutable patch가 이미 공개된 경우에도 그것은 "새로운
증거"일 뿐이고, target 변경 권한이 아니다.

## Outcome

Publish skill에는 post-dependencies consumer sync gate를 보강했다.
핵심 규칙은 "later patch version을 임의 대체하지 말고, target 변경은
사용자 최신 지시나 명시 승인으로만 한다"이다.

이 lesson은 skill 문구만으로는 드러나지 않는 실패 모드를 남긴다. 앞으로
release train 중 patch가 추가로 보이면 즉시 checklist를 refresh하고,
consumer PR을 만들거나 test하기 전에 target row를 다시 확정해야 한다.

## Verification

- `bluetape4k-publish` skill 확인:
  - Post-dependencies consumer sync gate가 "requested for the train" target을
    기준으로 삼는다.
  - Later patch release가 보이면 target을 re-confirm하라고 명시한다.
- Existing lesson search:
  - `rg -n "1\\.3\\.1|1\\.3\\.0|consumer sync|consumer-sync|later patch|dependencies.*target" ...`
    결과 이 실패 모드에 대한 org-level lesson은 없었다.
- Documentation-only change:
  - `git diff --check`로 whitespace와 patch 형식을 검증한다.

## Future Guidance

Release consumer sync를 시작하기 전에 checklist에 다음 행을 반드시 적는다.

| Row | Required Evidence |
|---|---|
| Consumer target | `bluetape4k-dependencies` version from latest user instruction or checklist |
| Maven latest | Latest Maven Central-visible version, treated as evidence only |
| Target authority | User instruction, checklist, or explicit corrective-patch approval |
| Consumer scope | Repositories to update and repositories explicitly out of scope |
| Validation | Dependency resolution plus repo-level tests for each consumer |

If `consumer target` and `Maven latest` differ, stop consumer branch work. Report
both versions, explain why they differ, and proceed only after the latest user
instruction or checklist target is unambiguous.

Do not encode a different version in branch names, commit messages, PR titles,
or PR bodies until that row is settled. If the user says the examples should
only consume the train target, do not reinterpret the already-published patch as
a required consumer upgrade.
